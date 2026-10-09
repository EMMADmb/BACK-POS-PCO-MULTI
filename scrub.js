require('dotenv').config();
const { Client } = require('pg');

const client = new Client({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/postgres'
});

async function run() {
  await client.connect();
  await client.query("UPDATE pos_empresas SET nombre = 'Empresa Demo S.A.' WHERE nombre ILIKE '%Oaxaca%' OR nombre ILIKE '%Apicultores%'");
  await client.query("UPDATE pos_configuraciones SET empresa_nombre = 'Empresa Demo S.A.' WHERE empresa_nombre ILIKE '%Oaxaca%' OR empresa_nombre ILIKE '%AUP%'");
  console.log('Database scrubbed');
  await client.end();
}
run().catch(console.error);
