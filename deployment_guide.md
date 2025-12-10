# Deploying to Streamlit Community Cloud

Follow these steps to publish your Research Agent app to the internet.

## 1. Prepare your Repository

Streamlit Cloud deploys directly from your GitHub repository.

1.  **Commit your changes**:
    ```bash
    git add .
    git commit -m "Initial commit of Research Agent app"
    ```

2.  **Push to GitHub**:
    - Create a new repository on GitHub.
    - Follow the instructions to push your local repository to GitHub.
    ```bash
    git remote add origin <your-repo-url>
    git branch -M main
    git push -u origin main
    ```

## 2. Deploy on Streamlit Cloud

1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Sign in with your GitHub account.
3.  Click **"New app"**.
4.  Select your repository, branch (`main`), and the main file path (`app.py`).
5.  Click **"Deploy!"**.

## 3. Configure Secrets

Your app needs API keys to work. You must set these in the Streamlit Cloud dashboard.

1.  On your app's dashboard, click **"Manage app"** (bottom right) or the three dots menu -> **"Settings"**.
2.  Go to the **"Secrets"** tab.
3.  Paste your secrets in the TOML format:

    ```toml
    GOOGLE_API_KEY = "your-google-api-key-here"
    ```
    *(Copy the value from your local `.env` file, but do not include the `export` keyword if present).*

4.  Click **"Save"**.

## 4. Verify

Once deployed and secrets are saved, your app should automatically refresh and be ready to use!
