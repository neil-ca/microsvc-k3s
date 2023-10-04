use reqwest::Client;
use sqlx::PgPool;
use tracing::error;
use reqwest::StatusCode;
use std::thread::sleep as std_sleep;
use tokio::time::Duration;
use scraper::{Html, Selector};

use chrono::NaiveDate;
#[derive(Clone, Debug)]
struct Product {
    name: String,
    price: String,
    old_price: Option<String>,
    link: String,
}

async fn scrape(ctx: Client) -> Result<(), String> {
    let mut pagenum = 1;
    let mut retry_attempts = 0;
    let url = format!("https://www.amazon.com/s?k=raspberry+pi&page={pagenum}");

    let res = match ctx.get(url).send().await {
        Ok(res) => res,
        Err(e) => {
            error!("Error while attempting to send HTTP request: {e}");
            break
        }
    };
    if res.status() == StatusCode::SERVICE_UNAVAILABLE {
        error!("Amazon returned a 503 at page {pagenum}");
        retry_attempts += 1;
        if retry_attempts >= 10 {
            error!("It look like amazon is bloking us! we will rest for an hour.");
            std_sleep(Duration::from_secs(3600));
            continue;
        } else {
            std_sleep(Duration::from_secs(15));
            continue;
        }
    }

    retry_attempts = 0;
    let res = match res.text().await {
        Ok(res) => res,
        Err(e) => {
            error!("Error while attemting to get HTTP body: {e}");
            break
        }
    };
}
struct CustomService {
    ctx: Client,
    db: PgPool,
}

const USER_AGENT: &str = "Mozilla/5.0 (linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0)";

#[shuttle_runtime::async_trait]

impl shuttle_runtime::Service for CustomService {
    async fn bind(mut self, _addr: std::net::SocketAddr) -> Result<(), shuttle_runtime::Error> {
        // Start your service and bind to the socket address
        scrape(self.ctx, self.db)
            .await
            .expect("scrapping should not finish");
        error!("The web scrapper loop shouldn't finish!");
        Ok(())
    }
}
#[shuttle_runtime::main]
async fn main(
    #[shuttle_shared_db::Postgres] db: PgPool,
) -> Result<CustomService, shuttle_runtime::Error> {
    let ctx = Client::builder().user_agent(USER_AGENT).build().unwrap();
    Ok(CustomService { ctx, db })
}
