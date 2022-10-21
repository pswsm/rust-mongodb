use actix_web::{
    get,
    App,
    HttpServer,
    Responder,
    HttpResponse
};
mod db_connection;


#[get("/api/tables")]
async fn tables() -> impl Responder {
    format!("Techniaclly speaking, this is ok")
}

#[get("/api/results")]
async fn results() -> impl Responder {
    let scores: Vec<db_connection::Model> = db_connection::get_scores().await.unwrap_or_else(|_| vec![db_connection::Model::default()]);
    println!("{:?}", scores);
    HttpResponse::Ok().json(scores)
}

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(tables)
            .service(results)
    })
    .bind(("127.0.0.1", 3000))?
    .run()
    .await
}
