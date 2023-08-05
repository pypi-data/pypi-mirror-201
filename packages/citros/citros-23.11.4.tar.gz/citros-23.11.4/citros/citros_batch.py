class citros_batch():
    def __init__(self, citros):
        self.citros = citros      
        self.log = citros.log
                        
    def get_batch(self, batch_run_id):
        query = """
        query getData($batchRunId: UUID!) {
            batchRun(id: $batchRunId) {
                id                
                completions
                parallelism                
                simulation {
                    id
                    timeout
                    launch {
                        id
                        name
                        package {
                            id
                            name
                        }
                    }
                }
            }            
        }
        """
        result = self.citros.gql_execute(query, variable_values={"batchRunId": batch_run_id})
        return result
        
   
   