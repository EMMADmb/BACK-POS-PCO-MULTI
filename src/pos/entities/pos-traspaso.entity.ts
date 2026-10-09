import { Entity, Column, PrimaryGeneratedColumn, CreateDateColumn, ManyToOne, JoinColumn, OneToMany } from 'typeorm';
import { PosSucursal } from './pos-sucursal.entity';
import { PosUsuario } from './pos-usuario.entity';
import { PosTraspasoDetalle } from './pos-traspaso-detalle.entity';

@Entity('pos_traspasos')
export class PosTraspaso {
  @PrimaryGeneratedColumn({ name: 'id_traspaso' })
  idTraspaso: number;

  @Column({ length: 50, unique: true })
  folio: string;

  @ManyToOne(() => PosSucursal, { nullable: false })
  @JoinColumn({ name: 'id_sucursal_origen' })
  sucursalOrigen: PosSucursal;

  @ManyToOne(() => PosSucursal, { nullable: false })
  @JoinColumn({ name: 'id_sucursal_destino' })
  sucursalDestino: PosSucursal;

  @ManyToOne(() => PosUsuario, { nullable: false })
  @JoinColumn({ name: 'id_usuario' })
  usuario: PosUsuario;

  @CreateDateColumn({ name: 'fecha' })
  fecha: Date;

  @Column({ length: 20, default: 'Completado' })
  estatus: string; // 'Completado', 'Cancelado'

  @Column('text', { nullable: true })
  observaciones: string;

  // --- NUEVOS CAMPOS PARA TRASPASOS AVANZADOS ---

  @Column({ length: 30, default: 'Simple' })
  tipoTraspaso: string; // 'Simple', 'ConCosto', 'Intercambio'

  @Column('decimal', { precision: 10, scale: 2, default: 0.00 })
  montoTotal: number;

  @Column({ length: 30, nullable: true })
  metodoPago: string; // 'Efectivo', 'Transferencia', etc. (Solo si es ConCosto)

  @Column({ nullable: true })
  idTraspasoRelacionado: number; // Para ligar dos traspasos en un Intercambio

  // ----------------------------------------------

  @OneToMany(() => PosTraspasoDetalle, detalle => detalle.traspaso)
  detalles: PosTraspasoDetalle[];
}
