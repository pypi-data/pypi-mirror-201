from io import StringIO
import traceback
import datetime 
import sqlite3
import json
import os

#
# MONGO
# 
class BagReaderSQL():
    def read_messages(self, input_bag, simulation_run_id):
        from rosidl_runtime_py.convert import get_message_slot_types, message_to_yaml, message_to_csv, message_to_ordereddict
        from rosidl_runtime_py.utilities import get_message
        from rclpy.serialization import deserialize_message

        buffer = StringIO()            
        
        self.conn = sqlite3.connect(input_bag)
        self.cursor = self.conn.cursor()

        topics_data = self.cursor.execute("SELECT id, name, type FROM topics").fetchall()
        self.topics = {name_of:{'type':type_of, 'id':id_of, 'message':get_message(type_of) } for id_of,name_of,type_of in topics_data}

        for topic_name in self.topics.keys():
            rows = self.cursor.execute(f"select id, timestamp, data from messages where topic_id = {self.topics[topic_name]['id']}").fetchall()
            my_list = []
            rid = 0
            for id, timestamp, data in rows:
                d_data = deserialize_message(data, self.topics[topic_name]["message"])
                msg_dict = message_to_ordereddict(d_data)
                json_data = json.dumps(msg_dict)
                
                row = chr(0x1E).join([f"{simulation_run_id}", f"{rid}", f"{timestamp}", f"{topic_name}", f"{self.topics[topic_name]['type']}", f"{json_data}\n"])            
                rid = rid + 1
                buffer.write(row) 
        return buffer
                        