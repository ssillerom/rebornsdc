pragma solidity >=0.7.0;

import "./registroUsuarios.sol";


contract Transacciones is registroUsuarios {

/** Definimos las variables de nuestro contrato */

    struct VentaOrden {
    address productor;
    uint32 precio;
    uint64 energia;
    uint64 timestamp;
  }

  struct CompraOrden {
    address productor;
    uint32 precio;
    uint64 energia;
    address usuarioAddress;
    uint64 timestamp;
  }

  /**Añadimos la dirección del productor *** Se ha añadido una dirección de Metamask *** 
    ¿Qué es metamask?
    https://metamask.io/
  
  */

  VentaOrden[] public ordenesVenta;
  CompraOrden[] public ordenesCompra;

  address public direccionProductor= 0xAB2143d2c4C336a2C7722940D41ef33CD1b68573;

  /** Primero vamos a registar la energia generada por el productor */

  CompraOrden[] public energiaProducida;

  mapping(address => uint) public indiceVenta;
  mapping(address => uint) public indiceCompra;
  
  event eventoVenta(address indexed productor,uint32 indexed precio, uint64 energia);

  event eventoCompra(address indexed productor,uint32 precio, uint64 energia, address usuarioAddress);

  function venderEnergia(uint32 precioVenta, uint64 energiaGenerada, uint64 timestampVenta) soloUsuariosRegistrados public {

    // registramos el orden de venta en nuestro indice de ventas

    uint ventaId = indiceVenta[msg.sender];

    /** Se requiere la venta minima de 2 Kw  */
    
    require(energiaGenerada >= 2);

    ordenesVenta.push(VentaOrden({
      productor: msg.sender,
      precio: precioVenta,
      energia: energiaGenerada,
      timestamp: timestampVenta
      }));

    emit eventoVenta(ordenesVenta[ventaId].productor, ordenesVenta[ventaId].precio, ordenesVenta[ventaId].energia);
  }

  function comprarEnergia(address productorCompra, uint32 precioCompra, uint64 energiaComprada, address addressComprador, uint64 fechaCompra) soloUsuariosRegistrados public {
    
    // entramos en el indice para ver las ofertas de venta de energia realizadas por el productor, productorCompra
    uint ventaId = indiceVenta[productorCompra];

    // requerimos que haya al menos una oferta
    require(0x0 != ventaId);

    // antes de registar la compra, revisamos que la oferta exista en el indice 
    if ((ordenesVenta.length > ventaId) && (ordenesVenta[ventaId].productor == productorCompra)) {

      // vemos si el precio de compra matchea con el precio al que se vendió, que sea distinto de 0 y que la energia comprada sea superior a 0.5 Kilowatios

      require(ordenesVenta[ventaId].precio == precioCompra && precioCompra > 0 && energiaComprada >= 1);

      indiceCompra[msg.sender] = ordenesCompra.length;

      // registramos el evento de compra de energia en el indice de compras
      ordenesCompra.push(CompraOrden({
        productor: productorCompra,
        precio: precioCompra,
        energia: energiaComprada,
        usuarioAddress: addressComprador,
        timestamp: fechaCompra
        }));

      emit eventoCompra(productorCompra, precioCompra, energiaComprada, addressComprador);

      // hacemos un check de la compra realizada por el consumidor y la guardamos
      require(ordenesCompra[ventaId].productor == direccionProductor);

      energiaProducida.push(CompraOrden({
        productor: productorCompra,
        precio: precioCompra,
        energia: energiaComprada,
        usuarioAddress: addressComprador,
        timestamp: fechaCompra
        }));

     } else {
         // si no la encontramos, revertimos la orden de compra
      revert();
    }
  }
}