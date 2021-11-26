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