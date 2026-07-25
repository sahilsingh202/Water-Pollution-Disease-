# Water Pollution & Disease — Streamlit Deployment

This deployment package was created from the project's Colab notebook.

## Required files

Keep these files in the same GitHub repository folder:

- `app.py`
- `train_model.py`
- `requirements.txt`
- `water_pollution_disease.csv`
- `water_disease_model.pkl` (created after training)

## Create the model

Place your original dataset in this folder and make sure its filename is exactly:

`water_pollution_disease.csv`

Then run:

```bash
pip install -r requirements.txt
python train_model.py
```

This creates:

`water_disease_model.pkl`

## Test Streamlit locally

```bash
streamlit run app.py
```

## Deploy

Push `app.py`, `requirements.txt`, `water_disease_model.pkl` and the other project files to GitHub. In Streamlit Community Cloud choose `app.py` as the main file.

The app uses relative paths instead of Google Colab `/content/drive/...` paths, which is necessary for deployment.
