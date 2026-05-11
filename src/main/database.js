const { Client } = require("pg")

const client = new Client({
    user: "postgres",
    host: "localhost",
    database: "mydb",
    password: "mypassword",
    port: 5432
})

client.connect()
    .then(() => {
        console.log("Connected to PostgreSQL")
    })
    .catch(err => {
        console.error(err)
    });

module.exports = {
    client
}


// const result = await client.query(
//     "SELECT * FROM users"
// )

// console.log(result.rows)