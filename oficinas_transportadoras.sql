use DataLakeVentas
select pco.id_ciudad,pca.ciudad,pca.departamento,pco.direccion,pco.telefonos,pca.transportadora,pca.estado
from plataforma_ciudades_oficinas pco
	INNER JOIN plataforma_ciudades_aveonline pca
	on pco.id_ciudad=pca.id_ciudad
where pca.estado='Activo' and pca.transportadora='Servientrega'
order by pca.ciudad