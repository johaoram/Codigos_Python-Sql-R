SELECT plataforma_carga_masiva.id_tienda_generado, plataforma_tiendas.id_asesor_comercial, plataforma_tiendas.lider, COUNT(*) AS Ventas
FROM plataforma_carga_masiva INNER JOIN plataforma_tiendas
ON plataforma_carga_masiva.id_tienda_generado = plataforma_tiendas.id_tienda
WHERE (plataforma_carga_masiva.fecha_creacion BETWEEN 20220901 AND 20220931 AND plataforma_carga_masiva.estado_transportadora = 'Entregada' AND plataforma_tiendas.id_asesor_comercial = '5')
GROUP BY plataforma_carga_masiva.id_tienda_generado, plataforma_tiendas.id_asesor_comercial, plataforma_tiendas.lider
ORDER BY ventas DESC