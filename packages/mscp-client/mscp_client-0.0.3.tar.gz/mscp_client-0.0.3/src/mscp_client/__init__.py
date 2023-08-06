from sqlalchemy import inspect, text
import pandas as pd
from sqlalchemy.dialects import mysql
import numpy as np
#Version 0.0.3
class Client:
    def __init__(self, engine):
        self.engine = engine

    def get_tables(self):
        """
        Returns a list of names of all tables in the 'mscp' schema of the database
        connected to the engine object.
        """
        table_list = []
        inspector = inspect(self.engine)
        for table_name in inspector.get_table_names(schema='mscp'):
            table_list.append(table_name)
        return table_list

    def get_name_ids(self, entity_types=None, rev=True):
        """
        Retrieves the names and ids of various entities in the database, such as
        loggers, stations, measurements, etc. Returns a dictionary where the keys
        are the entity types and the values are dictionaries containing the
        name-id pairs for each entity of that type. If entity_types is None,
        returns all entity types.
        """

        # Set the default entity_types if not provided by the user/other function
        entity_types = entity_types or [
            'loggers', 'stations', 'measurements', 'gs_types', 'sensor_types']

        # Create a dictionary of queries for each entity_type with the appropriate SELECT statement based on the entity_types list
        queries = {
            entity_type: text(f"SELECT {'type, id' if 'type' in entity_type else 'name, id'} FROM {entity_type}")
            for entity_type in entity_types
        }

        # Connect to the database engine
        with self.engine.connect() as connection:
            result = {}
            # Iterate through each entity_type and its corresponding query
            for entity_type, query in queries.items():
                # Execute the query to get the data from the database
                data = connection.execute(query)
                # Check if we need to reverse the dictionary key-value pairs ie. id-name instead of name-id
                if rev:
                    # If the entity_type contains 'type', use 'type' and 'id' as key-value pairs
                    # Otherwise, use 'name' and 'id' as key-value pairs
                    result[entity_type] = {type: id_ for type, id_ in data} if 'type' in entity_type else {name: id_ for name, id_ in data}
                else:
                    # If the entity_type contains 'type', use 'id' and 'type' as key-value pairs
                    # Otherwise, use 'id' and 'name' as key-value pairs
                    result[entity_type] = {id_: type for type, id_ in data} if 'type' in entity_type else {id_: name for name, id_ in data}
            # Return the result dictionary containing the mapping of ids to names/types (or reverse)
            return result

    def get_id_names(self, entity_types=None):
        return self.get_name_ids(entity_types, False)

    def render_legacy_gws(self, df):
        """
        Transforms a data frame containing new data into a legacy frame format.
        Returns a new data frame with the transformed data.
        """
        #First we fetch the lelel calcs from the db and put them in a dataframe
        q = "SELECT * FROM gws_level_calc"
        calcs_df = pd.read_sql_query(sql=text(q), con=self.engine.connect())

        #then we get a dict of ids to names and names to ids:
        id_to_names=self.get_id_names()
        names_to_ids=self.get_name_ids()

        # merge by station_id. This is nessicary to merge the start and end dates so we can compare dates later on.
        merged_data = pd.merge(df, calcs_df, on=['station_id'])

        # This is where we do date comparison to get the correct formula inputs.
        merged_data = merged_data[(merged_data['timestamp'] >= merged_data['start_date']) & (
            merged_data['timestamp'] <= merged_data['end_date'])]
        
        # Divide the monument_height_in by 12 to convert the height from inches to feet.
        # Divide the value by 25.4 to convert it from millimeters to inches, and then divide the result by 12 to convert it to feet.
        # Subtract the values obtained in steps 1 and 2 from the hang_length_ft values.
        merged_data['port1_dtw_ft'] = merged_data['hang_length_ft'] - \
            (merged_data['monument_height_in']/12) - \
            ((merged_data['value']/25.4)/12)

        # get the measurement_id for the 'Depth To Water In Feet' measurement
        dtw_id = names_to_ids["measurements"]['Depth To Water In Feet']
        water_level_id = names_to_ids["measurements"]['Water Level']
        # create a new DataFrame for the rows with measurement_id == 1.
        subset_df = merged_data[merged_data['measurement_id'] == water_level_id].copy()

        # set the measurement_id and value columns for the new rows
        subset_df.loc[:, 'measurement_id'] = dtw_id
        subset_df.loc[:, 'value'] = subset_df['port1_dtw_ft']

        # add the new rows back to the merged dataframe
        merged_df = pd.concat([merged_data, subset_df], ignore_index=True)

        # Map the ids to the names.
        merged_df["logger_id"] = merged_df["logger_id"].map(
            id_to_names["loggers"])
        merged_df["station_id"] = merged_df["station_id"].map(
            id_to_names["stations"])
        merged_df["measurement_id"] = merged_df["measurement_id"].map(
            id_to_names["measurements"])

        # Create a new column that combines measurement_id and port_number
        merged_df['measurement_port'] = merged_df['measurement_id'] + \
            ' port ' + merged_df['port_number'].astype(str)

        # Pivot the data frame for values so it is more like legacy data
        pivot = merged_df.pivot_table(index=['logger_id', 'station_id', 'timestamp'],
                                      columns='measurement_port',
                                      values='value')
        
        # Fill null values in 'qa_codes_id' column with a placeholder value, e.g., -1
        merged_df['qa_codes_id'] = merged_df['qa_codes_id'].fillna(-1)
        #Pivot the data frame for QAQC codes so it is more like legacy data
        qa_pivot = merged_df.pivot_table(index=['logger_id', 'station_id', 'timestamp'],
                            columns='measurement_port',
                            values='qa_codes_id',
                            aggfunc=lambda x: ' '.join(str(v) for v in x if v != -1))

        # Replace the placeholder values with null values after the pivot table is created
        qa_pivot = qa_pivot.replace(-1, np.nan)

        #Rename the columns so we know wich cols are values and wich are QAQC codes.
        qa_pivot.columns = ['QAQC ' + col for col in qa_pivot.columns]
        #Concat the two dataframes together and reset the index.
        result = pd.concat([pivot, qa_pivot], axis=1).reset_index()
        #Return the result
        return result
