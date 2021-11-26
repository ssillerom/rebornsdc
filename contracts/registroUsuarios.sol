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