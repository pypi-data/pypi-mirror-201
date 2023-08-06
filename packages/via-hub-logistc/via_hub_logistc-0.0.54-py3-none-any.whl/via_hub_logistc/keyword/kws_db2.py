import ibm_db

from robot.api.deco import keyword
from robot.api import Error


class ViaDb2():
    ### Return conncection with db2 ###
    @keyword(name="Db2 Connect To Database")
    def db2_connect_to_database(self, host, db_name, user_id, password):
        try:
            connString = f"ATTACH=FALSE;DATABASE={db_name};HOSTNAME={host};PROTOCOL=TCPIP;UID={user_id};PWD={password}"
            return ibm_db.connect(connString, '', '')
        except Exception as e:
            raise Error(e)
    
    ### Return json with result the of query ###
    @keyword(name="Db2 Execute Query")
    def db2_execute_query(self, connection, query):
        lsr_result = []

        try:
            stmt = ibm_db.exec_immediate(connection, query)
            result = ibm_db.fetch_assoc(stmt)

            while(result):
                if type(result) != bool:
                    lsr_result.append(result)

                result = ibm_db.fetch_assoc(stmt)

            return lsr_result
        except Exception as e:
            raise Error(e)
