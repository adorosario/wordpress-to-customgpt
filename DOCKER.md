# Docker Guide for wordpress-to-customgpt

This guide provides instructions on how to build and run the Docker container for the wordpress-to-customgpt project locally, as well as how to deploy it to Heroku.

## Prerequisites

- Docker installed on your local machine
- Heroku CLI installed (for Heroku deployment)
- Git installed

## Building and Running Locally

1. Clone the repository:
   ```
   git clone https://github.com/your-username/wordpress-to-customgpt.git
   cd wordpress-to-customgpt
   ```

2. Build the Docker image:
   ```
   docker build -t wordpress-to-customgpt .
   ```

3. Run the container locally:
   ```
   docker run -p 8501:8501 -v $(pwd):/app wordpress-to-customgpt streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501` to access the Streamlit app.

## Deploying to Heroku

### Option 1: Heroku Git Deployment

1. Login to Heroku CLI:
   ```
   heroku login
   ```

2. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

3. Set the stack to container:
   ```
   heroku stack:set container
   ```

4. Push to Heroku:
   ```
   git push heroku main
   ```

5. Open the app in your browser:
   ```
   heroku open
   ```

### Option 2: Heroku Container Registry

1. Login to Heroku Container Registry:
   ```
   heroku container:login
   ```

2. Create a new Heroku app (if not already created):
   ```
   heroku create your-app-name
   ```

3. Build and push the Docker image to Heroku:
   ```
   heroku container:push web -a your-app-name
   ```

4. Release the container:
   ```
   heroku container:release web -a your-app-name
   ```

5. Open the app in your browser:
   ```
   heroku open -a your-app-name
   ```

## Troubleshooting

- If you encounter any issues with port binding on Heroku, make sure your `app.py` is using the `$PORT` environment variable:

  ```python
  import os
  port = int(os.environ.get("PORT", 8501))
  st.run(app, port=port)
  ```

- If your app is crashing on Heroku, check the logs:
  ```
  heroku logs --tail -a your-app-name
  ```

## Additional Notes

- Remember to update your `requirements.txt` file if you add any new dependencies to your project.
- You may need to configure environment variables in Heroku for any sensitive information (like API keys) that your app requires. You can do this through the Heroku Dashboard or using the Heroku CLI:
  ```
  heroku config:set VARIABLE_NAME=value -a your-app-name
  ```

For more information on deploying Streamlit apps to Heroku, refer to the [Streamlit documentation](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker) and [Heroku documentation](https://devcenter.heroku.com/categories/deploying-with-docker).
