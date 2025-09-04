# Predefined Questions
general_questions = [
    "Summarize the uploaded documents.",
    "List the key highlights of this agreement",
    "What is the exact submission due date and time?",
    "Is it a pickup or delivery model, or both?",
    "Are there any constraints related to shipping? If yes, give me all the constraints related to shipping.",
    "Are there any conditions on product design? If yes, give me all the constraints related to product design.",
    "What is the required temperature for storage or transportation?",
    "When is the RFI due date or deadline, if applicable?",
    "What is the total size of opportunity in terms of dollars?",
    "Do we need to submit the bid for all the products?",
    "What are the categories covered by the bid?",
    "Are there any certifications needed?", 
    "When is the RFI due date or deadline, if applicable?",
    "When is the RFP due date or deadline?",
    "When is the sample due date or deadline?",
    "What is the number of samples required?",
    "What is the sample shipping address?",
    "What are the payment terms?",
    "What is the artwork or design fees?",
    "What are the testing requirements?",
    "What is the testing fees?",
    "Is there any brokrage, if applicable?",
    "What is the product assortment?",
    "What are the product categories covered by the bid?",
    "Is there any miscellaneous fees?",
    "Are there any audits needed?",
    "What are customer DC locations?",
    "What is the volume split by DC locations?",
    "Can we resubmit the bid?",
    "On what criteria is the bid awarded?"
]

shipping_logistics_questions = [
    "What are the EDI setup requirements.",
    "What are the standard freight terms.",
    "What are the fill rate requirements",
    "What are the damage policies",
    "Does the customer have any preferred carriers?",
    "What are the palletization requirements?",
    "Summarize the labeling and documentation requirements",
    "What is the process for scheduling appointments?",
    "List all fees for non-compliance",
    "Are there any constraints related to shipping? If yes, give me all the constraints related to shipping."
]

bid_rfi_rfp_questions = [
    "Summarize the uploaded documents.",
    "List the key highlights of this agreement",
    "What are the categories covered by the bid?",
    "What is the exact submission due date and time?",
    "What are the freight terms? Is it a pickup or delivery model, or both?",
    "Are there any conditions on product design? If yes, give me all the constraints related to product design.",
    "When is the RFI due date or deadline, if applicable?",
    "What is the total size of opportunity in terms of dollars?",
    "Are there any audits or certifications required?",
    "When is the RFI due date or deadline, if applicable?",
    "When is the RFP due date or deadline?",
    "When is the sample due date or deadline?",
    "What is the number of samples required?",
    "What is the sample shipping address?",
    "What are the payment terms?",
    "What are the artwork and/or design fees?",
    "What are the testing requirements? Will we be responsible for paying testing fees?",
    "Is there any brokerage, if applicable?",
    "Are there any miscellaneous fees?",
    "What are customer DC locations?",
    "What is the volume split by DC locations?",
    "On what criteria is the bid awarded?",
    "Is there any marketing cost or fund per item needs to included in pricing?",
    "what is the design artwork cost per item?",
    "Is there any reclamation cost included in this bid?"
]

contract_questions = [
    "What are the agreed pricing terms for the products or services? Detail any fixed pricing, variable pricing structures, or volume-based discounts.",
    "Are there provisions for price adjustments or price locks? Are there provisions for price adjustments or price locks?",
    "What are the payment terms and timelines? Summarize due dates, payment methods, and penalties for late payments.",
    "Are there any rebates or discounts offered, and what are the conditions? Note volume-based rebates, early payment discounts, or other incentives.",
    "What are the terms regarding freight, shipping, and logistics? Clarify who bears the shipping costs, delivery schedules, and responsibilities in case of delays.",
    "Are there penalties or fees for failure to meet delivery deadlines or quality standards? Identify any charges for late deliveries or substandard products.",
    "Are there provisions for minimum order quantities or commitments? Note any contractual obligations for minimum purchases or inventory levels.",
    "What is the policy on returns, replacements, or damaged goods? Detail the process, timelines, and costs associated with product returns or replacements.",
    "What are the requirements for notice periods regarding price changes or termination? Identify the lead time needed to communicate price adjustments or end the contract.",
    "Are there any performance guarantees or penalties tied to service levels or delivery? Highlight any service-level agreements (SLAs) or related performance metrics."
]


'''
General Bid

RFI Due Date / Deadline (If Applicable)           --> When is the RFI due date or deadline, if applicable?
RFP Due Date / Deadline              --> When is the RFP due date or deadline?
Sample Due Date / Deadline           --> When is the sample due date or deadline?
Number of samples required           --> What is the number of samples required?
Samples Shipping Address             --> What is the sample shipping address?
Payment Terms                        --> What are the payment terms?
Artwork / Design Fees                --> What is the artwork or design fees?
Testing Requirements                 --> What are the testing requirements?
Testing Fees                         --> What is the testing fees?
Brokerage (if applicable)            --> Is there any brokrage, if applicable?
Product Assortment                   --> What is the product assortment?
Categories covered by bid            --> What are the categories covered by the bid?
Other miscellaneous fees             --> Is there any miscellaneous fees?
Pricing required (FTL/LTL/FOB Pickup)--> 
Certifications needed                --> Are there any certifications needed?
Audits needed                        --> Are there any audits needed?
Customer DC Locations                --> What are customer DC locations?
Volume Split by DC locations         --> What is the volume split by DC locations?
Total size ($) of opportunity        --> What is the total size of opportunity?      #####


Can we resubmit the bid?
On what criteria is the bid awarded?


Product Specific

Number of products in bid
Product Pack configurations
Product Case configurations
Product specifications (materials, size, weight, etc.)
Estimated annual volumes per item
Estimated annual volumes total
National Brand Equivalents (NBE's)
Primary and Secondary packaging requirements
'''