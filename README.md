# ems_api
## Ecommerce Management System - currently for Bath&amp;Bark 

## Project Structure
The structure of this api project repo is based from the [FastAPI Best Practices Project Structure](https://github.com/zhanymkanov/fastapi-best-practices). Each package has its own following files depending on its requirements:
- router.py - core of each module which contains all the endpoints 
- schemas.py - for pydantic models 
- models.py - for db models
- service.py - module-specific business logic
- dependencies.py - router dependencies
- constants.py - module specific constants and error codes 
- config.py - module-specific configurations and environment variables 
- utils.py - non-business logic functions / helper functions (e.g. response normalizatoin, data enrichment, etc.)
- exceptions.py - module-specific exceptions (e.g. `PostNotFound`, `InvalidUserData`)

Personally, it is also better to add a global version of these files, which is stored in the root `/src` directory, if there a lot of methods / constants that must be globally available. If there is not much, you can just reference other module into another moodule. 