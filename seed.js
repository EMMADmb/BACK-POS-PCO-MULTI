const { Client } = require('pg');
require('dotenv').config();

const client = new Client({
  connectionString: 'postgresql://postgres.ugxbeygatdohgsukvcpm:' + process.env.DB_PASSWORD + '@aws-0-us-east-1.pooler.supabase.com:5432/postgres'
});

async function run() {
  try {
    await client.connect();
    await client.query(`
      INSERT INTO pos_usuarios (nombre_completo, nombre_usuario, contrasena_hash, rol, activo)
      VALUES ('Super Administrador', 'Superadmin', '12345.', 'Soporte', true)
      ON CONFLICT (nombre_usuario) DO NOTHING;
    `);
    console.log('Usuario Superadmin insertado correctamente!');
  } catch (err) {
    console.error('Error insertando usuario:', err.message);
  } finally {
    await client.end();
  }
}

run();
