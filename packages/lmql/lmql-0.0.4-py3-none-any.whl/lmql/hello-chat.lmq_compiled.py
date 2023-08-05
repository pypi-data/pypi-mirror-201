import lmql.runtime.lmql_runtime as lmql
@lmql.query(None)
async def query(context=None):
   context.set_model('openai/gpt-3.5-turbo')
   context.set_decoder('argmax', )
   # where
   context.set_where_clause(None)
   # prompt
   (yield context.query(f'Hello[WHO]'))
   WHO = context.get_var('WHO')
   yield ('result', context.get_return_value())
