SELECT DAY(plataforma_carga_masiva.fecha_creacion) AS dia, plataforma_carga_masiva.id_tienda_generado, COUNT(*) AS Ventas
FROM plataforma_carga_masiva inner join plataforma_tiendas
ON plataforma_carga_masiva.id_tienda_generado = plataforma_tiendas.id_tienda
WHERE (plataforma_carga_masiva.fecha_creacion BETWEEN 20220901 AND 20220931 AND (plataforma_carga_masiva.estado = 'Activo' OR plataforma_carga_masiva.estado = 'Despachado') AND plataforma_tiendas.id_asesor_comercial = '5')
GROUP BY DAY(plataforma_carga_masiva.fecha_creacion), plataforma_carga_masiva.id_tienda_generado
ORDER BY dia