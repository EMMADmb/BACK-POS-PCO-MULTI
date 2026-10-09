import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, JoinColumn, OneToMany, Index } from 'typeorm';
import { PosEmpresa } from './pos-empresa.entity';
import { PosCategoria } from './pos-categoria.entity';
import { PosProductoCodigo } from './pos-producto-codigo.entity';
import { PosInventario } from './pos-inventario.entity';

@Entity('pos_productos')
@Index('UQ_codigo_empresa', ['codigoBarras', 'empresa'], { unique: true })
export class PosProducto {
  @PrimaryGeneratedColumn({ name: 'id_producto' })
  idProducto: number;

  @Column({ name: 'codigo_barras', length: 100, nullable: true })
  codigoBarras: string;

  @Column({ length: 255 })
  nombre: string;

  @Column({ type: 'text', nullable: true })
  descripcion: string;

  @Column({ type: 'text', nullable: true })
  aliasBusqueda: string;

  @Column('decimal', { name: 'precio_unitario', precision: 10, scale: 2, default: 0.00 })
  precioUnitario: number;

  @Column('decimal', { precision: 5, scale: 2, default: 0.00 })
  iva: number;

  @Column('decimal', { name: 'precio_publico', precision: 10, scale: 2, default: 0.00 })
  precioPublico: number;

  @Column('decimal', { name: 'precio_compra', precision: 10, scale: 2, default: 0.00 })
  precioCompra: number;

  @Column('decimal', { precision: 5, scale: 2, default: 18.0 })
  utilidad: number;

  @Column({ name: 'aplica_descuento', default: false })
  aplicaDescuento: boolean;

  @Column({ name: 'tipo_descuento', length: 20, default: 'porcentaje', nullable: true })
  tipoDescuento: string;

  @Column({ name: 'aplica_iva', default: false })
  aplicaIva: boolean;

  @Column('decimal', { name: 'precio_venta', precision: 10, scale: 2, default: 0.00 })
  precioVenta: number;

  @Column('decimal', { name: 'precio_mayoreo', precision: 10, scale: 2, nullable: true })
  precioMayoreo: number;

  @Column('decimal', { precision: 10, scale: 2, default: 0.00 })
  descuento: number;

  @Column('decimal', { name: 'minimo_mayoreo', precision: 10, scale: 2, default: 0.00 })
  minimoMayoreo: number;

  @Column({ name: 'imagen_url', length: 255, nullable: true })
  imagenUrl: string;

  @Column({ name: 'clave_prod_serv', length: 20, default: '01010101' })
  claveProdServ: string;

  @Column({ name: 'clave_unidad', length: 10, default: 'H87' })
  claveUnidad: string;

  @Column({ name: 'tipo_articulo', length: 50, default: 'Terminado' })
  tipoArticulo: string;

  @Column({ name: 'unidad_medida', length: 20, default: 'Pza' })
  unidadMedida: string;

  @ManyToOne(() => PosCategoria, (categoria) => categoria.productos, { nullable: true, onDelete: 'SET NULL' })
  @JoinColumn({ name: 'id_categoria' })
  categoria: PosCategoria;

  @Column({ default: true })
  activo: boolean;

  @ManyToOne(() => PosEmpresa)
  @JoinColumn({ name: 'id_empresa' })
  empresa: PosEmpresa;

  @OneToMany(() => PosProductoCodigo, codigo => codigo.producto, { cascade: true })
  codigosAdicionales: PosProductoCodigo[];

  @OneToMany(() => PosInventario, inv => inv.producto, { cascade: true })
  inventarios: PosInventario[];
}
