## Tranxpert Dash Application

This package contains the code for the Dash application of Tranxpert system users.


#### Structure of this Dash Application

For the sake of maintenance, the following guidelines are enforced 
in the code on this folder:

1. The Main Application provides a Navigation Bar ([dbc.Sidebar](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/)).
This navigation bar is the interactive way to move around "Views" in the Single Page App served by dash:
  
   - `"/"`: The empty `pathname` refers to the home page of the application.
   - **Any other view will be located in a corresponding `pathname`**. For example: `"/vibration-analysis"` for the 
    vibration analysis view. 
     
    -   The code for a specific view is located under the `pages` folder. Each page contains all the 
    declarative flow of that page, **including components and callbacks**. For more information, read: https://dash.plotly.com/urls 
        
3. The main code of the application is a single declarative script in `main_app.py`. 
This code will register all the Dash callbacks for runtime.  
