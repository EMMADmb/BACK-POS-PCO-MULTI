import { Entity, Column, PrimaryGeneratedColumn, CreateDateColumn, OneToMany } from 'typeorm';
import { PosSucursal } from './pos-sucursal.entity';

@Entity('pos_empresas')
export class PosEmpresa {
  @PrimaryGeneratedColumn({ name: 'id_empresa' })
  idEmpresa: number;

  @Column({ length: 255 })
  nombre: string;

  @Column({ type: 'text', nullable: true })
  logoUrl: string;

  @Column({ length: 20, default: '#f59e0b' }) // Default Amber-500
  colorPrimario: string;

  @Column({ length: 20, default: '#333333' })
  colorSecundario: string;

  @Column({ length: 20, nullable: true })
  rfc: string;

  @Column({ length: 255, nullable: true })
  razonSocial: string;

  @Column({ default: true })
  activa: boolean;

  @CreateDateColumn({ name: 'fecha_creacion' })
  fechaCreacion: Date;

  @OneToMany(() => PosSucursal, (sucursal) => sucursal.empresa)
  sucursales: PosSucursal[];
}
