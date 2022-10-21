use serde::{Serialize, Deserialize};
use mongodb::{
    Client,
    bson::doc,
    options::FindOptions
};
use futures::stream::StreamExt;
use anyhow::Result;

const MONGODB_URI: &str = env!("MONGO_URI", "URI no available");

#[derive(Default, Serialize, Deserialize, Debug)]
enum ScoreTypes {
    F1,
    Accuracy,
    Combined,
    Exact,
    #[default]
    NA
}

#[derive(Default, Serialize, Deserialize, Debug)]
struct Score {
    score_type: ScoreTypes,
    score: f32
}

#[derive(Default, Serialize, Deserialize, Debug)]
pub struct Model {
    email: String,
    model_name: String,
    research_group: String,
    url: String,
    sts_ca: Score,
    pos: Score,
    catalanqa: Score,
    xquad: Score,
    tecla: Score,
    teca: Score,
    ancora: Score,
    sum: f32
}

pub async fn get_scores() -> Result<Vec<Model>> {
    let db = Client::with_uri_str(MONGODB_URI).await;
    let collection: mongodb::Collection<Model> = db.expect("DB not connected").database("club_benchmark").collection("evaluations");
    let filter: mongodb::bson::document::Document = doc! { "_id": 0, "__v": 0, "email": 0 };
    let find_options: FindOptions = FindOptions::builder().sort(doc! { "sum": -1 }).build();
    let cursor = collection.find(filter, find_options).await.ok().expect("Error getting entries");
    let see = cursor.map(|c| c.unwrap_or_else(|_| Model::default())).collect().await;
    Ok(see)
}
