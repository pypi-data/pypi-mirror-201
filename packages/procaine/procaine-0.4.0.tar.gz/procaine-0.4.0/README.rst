Procaine
========

**Procaine** is a REST client library for SAP AI Core API.  Reduces the pain.


Installation
------------

To use *Procaine*, first install it using pip:

.. code-block:: console

   $ pip install procaine


Usage
-----

Run a flow::

  >>> from procaine import aicore

  >>> auth = {"url": AUTH_URL, "clientid": CLIENT_ID, "clientsecret": CLIENT_SECRET}
  >>> api = aicore.Client(AI_API_URL, auth)

  >>> hello = api.create_execution("hello-world")
  >>> hello
  {'id': 'e96bc32ee9bf9e63', 'message': 'Execution scheduled', 'status': 'UNKNOWN', 'targetStatus': 'COMPLETED'}

  >>> api.execution(hello)
  { ... 'status': 'COMPLETED', ... 'targetStatus': 'COMPLETED'}
  
  >>> logs = api.execution_logs(hello)
  >>> print(logs)
   _____________ 
  < hello world >
   ------------- 
      \
       \
	\     
		      ##        .            
		## ## ##       ==            
	     ## ## ## ##      ===            
	 /""""""""""""""""___/ ===        
    ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~   
	 \______ o          __/            
	  \    \        __/             
	    \____\______/   


Documentation
-------------

More usage examples and detailed documentation could be found on https://procaine.readthedocs.io/
