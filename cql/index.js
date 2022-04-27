// ”cassandra-driver” is in the node_modules folder. Redirect if necessary.
let cassandra = require('cassandra-driver');
const executeConcurrent = cassandra.concurrent.executeConcurrent;
// Replace 'Username' and 'Password' with the username and password from your cluster settings
let authProvider = new cassandra.auth.PlainTextAuthProvider('cassendra', 'cassendra');
// Replace the PublicIPs with the IP addresses of your clusters
let contactPoints = ['127.0.0.1:9042'];
// Replace DataCenter with the name of your data center, for example: 'AWS_VPC_US_EAST_1'
let localDataCenter = 'datacenter1';
const createksQuery = "CREATE KEYSPACE IF NOT EXISTS grocery WITH REPLICATION = {'class' : 'SimpleStrategy','replication_factor' : 1};"
const createTableQuery = "CREATE TABLE IF NOT EXISTS grocery.fruit_stock (item_id TEXT, name TEXT, price_p_item DECIMAL, PRIMARY KEY (item_id));";
const insertQuery = 'INSERT INTO grocery.fruit_stock (item_id, name, price_p_item) VALUES (?, ?, ?) IF NOT EXISTS';
const useQuery = 'USE grocery'
let client = new cassandra.Client({contactPoints: contactPoints, authProvider: authProvider, localDataCenter: localDataCenter});
let ex = async()=>{
    client.connect()
    .then(()=>client.execute(createksQuery)
    .then(()=>client.execute(createTableQuery)))
    
    const values = [['a0','apples',0.50],['b1','bananas',0.40],['c3','oranges',0.35]]
    await executeConcurrent(client, insertQuery, values);

    console.log(`Finished executing ${values.length} queries with a concurrency`)

    await client.eachRow('SELECT name FROM grocery.fruit_stock',(n,row)=>{console.log(`This fruit name is ${row.name}`)})
    
} 
ex();

// Exit the program after all queries are complete
