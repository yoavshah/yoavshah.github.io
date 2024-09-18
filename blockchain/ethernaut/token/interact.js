const { ethers } = require("hardhat");

// npx hardhat console --network localhost
// npx hardhat run --network localhost scripts/interact.js
async function main () {
    const address = '0x959922bE3CAee4b8Cd9a407cc3ac1C251C2007B1';
    const TestContract = await ethers.getContractFactory('TestContract');
    const testContract = TestContract.attach(address);

    const [owner, addr1, addr2] = await ethers.getSigners();

    console.log(await testContract.balanceOf(addr1));

    result = await testContract.connect(addr1).transfer(addr2, 21n);

    balance = await testContract.balanceOf(addr1);
    console.log(balance)
}



main()
.then(() => process.exit(0))
.catch(error => {
    console.error(error);
    process.exit(1);
});