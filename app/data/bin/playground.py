import streamlit as st
import pandas as pd

from streamlit_ace import st_ace

def app():
    st.header("Green Chain Smarts Contracts playground")

    menu2 = ['registroUsuarios', 'Transacciones',
             'Token', 'Migration']

    choice = st.selectbox(
        'Seleccione el Smart Contract que desee ver: ', menu2)

    if choice == 'Transacciones':

      st.code("""
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
      """, language="python")

        # Spawn a new Ace editor
      content = st_ace()
  
    # Display editor's content as you type
      content

    elif choice == 'registroUsuarios':
      st.code("""
    pragma solidity >=0.7.0;

contract registroUsuarios {
    mapping (address => bool) registroUsuarios;
    address[] public usuario;

    constructor() public payable  {
    }

    function registrar() public payable{
        //* Se solicita un minimo de 0.001 de fee de GEC para poder registrarte como usuario de la red Green Energy Chain
        require(msg.value > .001 ether);
        registroUsuarios[msg.sender] = true;
        usuario.push(msg.sender);
    }

    //Aseguramos que solo los usuarios registrados en la red pueden suscribir ordenes
    modifier soloUsuariosRegistrados{
        require (registroUsuarios[msg.sender] == true);
        _;
    }
}
    """,language="python")
    # Spawn a new Ace editor
      content = st_ace()
  
    # Display editor's content as you type
      content


    elif choice == 'Token':
      pass

    elif choice == 'Migration':
      st.code("""
    
pragma solidity >=0.7.0;

contract Migrations {
    address public owner;
    uint public last_completed_migration_done;

    constructor() public {
        owner = msg.sender;
    }
    modifier restricted() {
        /** Esta función solo puede ser invocada por el dueño del contracto */
            if (msg.sender == owner) _;
    }
    function setCompleted(uint completed) public restricted {
        last_completed_migration_done = completed;
    }
    function upgrade(address new_address) public restricted {
        Migrations upgraded = Migrations(new_address);
        upgraded.setCompleted(last_completed_migration_done);
    }
}
    
    
    
    """,language="python")

        # Spawn a new Ace editor
      content = st_ace()
  
    # Display editor's content as you type
      content
        
