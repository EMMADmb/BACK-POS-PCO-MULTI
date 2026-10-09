const { Client } = require('pg');
require('dotenv').config();

const client = new Client({
  connectionString: 'postgresql://postgres.ugxbeygatdohgsukvcpm:' + process.env.DB_PASSWORD + '@aws-0-us-east-1.pooler.supabase.com:5432/postgres'
});

async function run() {
  try {
    await client.connect();
    
    // ==========================================
    // EMPRESA 1: Ferretería (Rojo)
    // ==========================================
    const resEmp1 = await client.query(`
      INSERT INTO pos_empresas (nombre, "logoUrl", "colorPrimario", "colorSecundario", rfc, "razonSocial", activa)
      VALUES ('Ferretería El Tornillo', 'https://cdn-icons-png.flaticon.com/512/3095/3095894.png', '#DC2626', '#991B1B', 'FERR990101', 'Tornillos SA de CV', true)
      RETURNING id_empresa;
    `);
    const idEmp1 = resEmp1.rows[0].id_empresa;

    const resSuc1 = await client.query(`
      INSERT INTO pos_sucursales (nombre, id_empresa, activo)
      VALUES ('Matriz Centro', $1, true)
      RETURNING id_sucursal;
    `, [idEmp1]);
    const idSuc1 = resSuc1.rows[0].id_sucursal;

    await client.query(`
      INSERT INTO pos_configuracion (id_sucursal, mensaje_ticket, ancho_ticket, direccion, telefono)
      VALUES ($1, '¡Gracias por construir con nosotros!', '58mm', 'Av. Las Palmas 123', '555-1234');
    `, [idSuc1]);

    await client.query(`
      INSERT INTO pos_usuarios (nombre_completo, nombre_usuario, contrasena_hash, rol, activo, id_sucursal)
      VALUES ('Administrador Ferretería', 'Admin1', '12345.', 'Administrador', true, $1)
      ON CONFLICT (nombre_usuario) DO NOTHING;
    `, [idSuc1]);

    // ==========================================
    // EMPRESA 2: Farmacia (Verde)
    // ==========================================
    const resEmp2 = await client.query(`
      INSERT INTO pos_empresas (nombre, "logoUrl", "colorPrimario", "colorSecundario", rfc, "razonSocial", activa)
      VALUES ('Farmacias La Salud', 'https://cdn-icons-png.flaticon.com/512/4320/4320337.png', '#059669', '#047857', 'FARM880202', 'Salud Total SA', true)
      RETURNING id_empresa;
    `);
    const idEmp2 = resEmp2.rows[0].id_empresa;

    const resSuc2 = await client.query(`
      INSERT INTO pos_sucursales (nombre, id_empresa, activo)
      VALUES ('Sucursal Norte', $1, true)
      RETURNING id_sucursal;
    `, [idEmp2]);
    const idSuc2 = resSuc2.rows[0].id_sucursal;

    await client.query(`
      INSERT INTO pos_configuracion (id_sucursal, mensaje_ticket, ancho_ticket, direccion, telefono)
      VALUES ($1, '¡Cuida tu salud con nosotros!', '80mm', 'Blvd. Hospitales 456', '555-9876');
    `, [idSuc2]);

    await client.query(`
      INSERT INTO pos_usuarios (nombre_completo, nombre_usuario, contrasena_hash, rol, activo, id_sucursal)
      VALUES ('Administrador Farmacia', 'Admin2', '12345.', 'Administrador', true, $1)
      ON CONFLICT (nombre_usuario) DO NOTHING;
    `, [idSuc2]);

    console.log('¡Datos de prueba insertados correctamente!');
  } catch (err) {
    console.error('Error insertando datos:', err);
  } finally {
    await client.end();
  }
}

run();
