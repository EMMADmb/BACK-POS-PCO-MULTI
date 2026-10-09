import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, JoinColumn, Index } from 'typeorm';
import { PosProducto } from './pos-producto.entity';
import { PosSucursal } from './pos-sucursal.entity';

@Entity('pos_inventarios')
@Index('UQ_producto_sucursal', ['producto', 'sucursal'], { unique: true })
export class PosInventario {
  @PrimaryGeneratedColumn('uuid')
  idInventario: string;

  @ManyToOne(() => PosProducto, p => p.inventarios, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'id_producto' })
  producto: PosProducto;

  @ManyToOne(() => PosSucursal, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'id_sucursal' })
  sucursal: PosSucursal;

  @Column('decimal', { name: 'stock_actual', precision: 10, scale: 2, default: 0.00 })
  stockActual: number;

  @Column('decimal', { name: 'stock_minimo', precision: 10, scale: 2, default: 0.00 })
  stockMinimo: number;

  @Column('decimal', { name: 'precio_venta_override', precision: 10, scale: 2, nullable: true })
  precioVentaOverride: number;
}
