use mongodb::{
    Client,
    options::ClientOptions
};
use tokio;
use std::error::Error;

const MONGODB_URI: &str = env!("MONGO_URI");

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let client_options: ClientOptions = ClientOptions::parse(MONGODB_URI).await?;
    let client: Client = Client::with_options(client_options)?;
    let databases: Vec<String> = client.list_database_names(None, None).await.unwrap_or_else(|_| Vec::new());
    let collections_0: Vec<String> = client.database(&databases[0]).list_collection_names(None).await.unwrap_or_else(|_| Vec::new());
    // println!("{:?}", collections_0);
    let evaluations: mongodb::Collection<_> = client.database(&databases[0]).collection(&collections_0[0]);
    Ok(())
}
