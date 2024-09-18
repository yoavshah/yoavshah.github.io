const { ethers } = require("hardhat");

// npx hardhat console --network localhost
// npx hardhat run --network localhost scripts/interact.js
async function main () {
    const address = '0x0DCd1Bf9A1b36cE34237eEaFef220932846BCD82';
    const TestContract = await ethers.getContractFactory('TestContract');
    const testContract = TestContract.attach(address);

    console.log(await testContract.owner());

    const [owner, addr1, addr2] = await ethers.getSigners();

    const TestContractHelper = await ethers.getContractFactory("TestContractHelper");
    const testContractHelper = await TestContractHelper.connect(addr1).deploy(address);
    await testContractHelper.waitForDeployment();

    console.log('TestContractHelper deployed to:', await testContractHelper.getAddress());

    console.log(await testContract.owner());
}



main()
.then(() => process.exit(0))
.catch(error => {
    console.error(error);
    process.exit(1);
});