pragma solidity ^0.4.2;

import "strings.sol";

contract HedgeContract1 {
  using strings for *;

  struct Investment {
    address investor;
    uint value;
    /*uint nowValue;*/
    /*uint holding;*/
    uint withdrawal;
    uint period; // in days
    uint withdrawalLimit;
    string blackListCompanies;
  }

  address public creator;
  address public investAgent;
  address public buyAgent;
  uint public minimumInvestment;
  uint public originalInvestment;

  // Performance indicators
  int public returnRatio;
  int public sharpe;
  int public alpha;
  int public beta;
  // TODO - Getters and setters

  Investment[] public investments;
  mapping (address => uint) pendingWithdrawals;

  // Events - publicize actions to external listeners
  event InvestmentOfferByBot(uint amount);
  event NewInvestmentByUser(address accountAddress, uint amount);

  // Helper function to guard functions
  modifier onlyBy(address _account)
  {
    if (msg.sender != _account)
        throw;
    _;
  }

  function HedgeContract1(
      uint _minimumInvestment,
      address _investAgent,
      address _buyAgent
    ) {
      // Set contract creator when creating the contract
      creator = msg.sender;
  }

  // Set new invest agent - only owner
  function setInvestAgent(address newInvestAgent)
    onlyBy(creator)
  {
    investAgent = newInvestAgent;
  }

  // Set new buy agent - only owner
  function setBuyAgent(address newBuyAgent)
    onlyBy(creator)
  {
    buyAgent = newBuyAgent;
  }

  // Set new minimum investment - only owner
  function setMinimumInvestment(uint newMinimumInvestment)
    onlyBy(creator)
  {
    // TODO - If its the same do not update to save gas
    minimumInvestment = newMinimumInvestment;
  }

  // Create a new investment
  function createInvestment(string companies) payable {
    if (msg.value < minimumInvestment) {
      throw;
    }

    // TODO - existing investment?
    // 3, 1 to change
    investments.push(Investment(msg.sender, msg.value, 0, 3, 1, companies));

    // Publish event
    NewInvestmentByUser(msg.sender, msg.value);
  }

  // Investment opportunity - only agent
  function investOffer(uint amount, string companies)
    onlyBy(investAgent)
  {
    if (this.balance < amount) {
      throw;
    }

    // TODO - implement criteria here
    var s = companies.toSlice();
    var delim = ",".toSlice();
    string[] memory parts = new string[](s.count(delim));
    for(uint i = 0; i < parts.length; i++) {
        parts[i] = s.split(delim).toString();
    }
    bool criteria = blackListCompaniesExists(parts);

    if (!criteria) {
      pendingWithdrawals[buyAgent] += amount;
      originalInvestment = amount;
      InvestmentOfferByBot(amount); // fire event
    } else {
      throw;
    }
  }

  function withdrawBuyAgent() onlyBy(buyAgent)
    returns (bool)
  {
        uint amount = pendingWithdrawals[msg.sender];

        pendingWithdrawals[msg.sender] = 0;
        if (msg.sender.send(amount)) {
            return true;
        } else {
            pendingWithdrawals[msg.sender] = amount;
            return false;
        }
  }

  function sendBuyAgent(int _returnRatio, int _sharpe, int _alpha, int _beta) payable
    onlyBy(buyAgent)
  {
    // Receive ether
    // Set financial indicators
    returnRatio = _returnRatio;
    sharpe = _sharpe;
    alpha = _alpha;
    beta = _beta;

    // Contract need to divide ether according to the share
    for(uint x = 0; x < investments.length; x++) {
      investments[x].withdrawal = investments[x].value / originalInvestment * msg.value; // TODO - Check truncations
      investments[x].value = 0;
    }
  }

  function blackListCompaniesExists(string[] companies) internal constant returns (bool)
  {
    bool found = false;
    var blackListCompanies = ",";

    for(uint x = 0; x < investments.length; x++) {
      blackListCompanies = blackListCompanies.toSlice().concat(investments[x].blackListCompanies.toSlice()).toSlice().concat(",".toSlice());
    }

    for(uint i = 0; i < companies.length; i++) {
      var comparison = ",".toSlice().concat(companies[i].toSlice()).toSlice().concat(",".toSlice());
      found = blackListCompanies.toSlice().contains(comparison.toSlice());

      if (found) {
          return true;
      }
    }

    return false;
  }

  function blackListCompanies() constant returns (string)
  {
    var s = ",";

    for(uint x = 0; x < investments.length; x++) {
      s = s.toSlice().concat(investments[x].blackListCompanies.toSlice()).toSlice().concat(",".toSlice());

      /*if(x != investments.length - 1) {
        s = s.toSlice().concat(",".toSlice());
      }*/
    }

    return s;
  }

  function availableForInvestment() constant returns (uint)
  {
    uint availableForInvestment;

    for(uint x = 0; x < investments.length; x++) {
      availableForInvestment += investments[x].value;
    }

    return availableForInvestment;
  }

  // Withdrawal by user
  function withdrawalUser(uint withdrawAmount) public returns (bool)
  {
    for(uint x = 0; x < investments.length; x++) {
      if (msg.sender == investments[x].investor) {
        uint amount = investments[x].withdrawal;

        investments[x].withdrawal = 0;
        if (msg.sender.send(amount)) {
            return true;
        } else {
            investments[x].withdrawal = amount;
            return false;
        }
        break;
      }
    }

    return false;
  }

  // Kill the contract and send the funds to creator
  // TODO - This has to be improved - send funds according to nowValue back to investors
  function kill() {
    if (msg.sender == creator) suicide(creator);
  }

  // TODO - get the values from the investments array
  // Get investment details from investments mapping
  function getInvestmentCurrentValue(address investor) constant
    returns(uint nowValue)
  {
    // nowValue = investments[investor].nowValue;
  }
}
