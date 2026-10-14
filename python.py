# 1. Calculate late fines for regular books with 18% tax
def calculateLateBookFine(a, b):
    subtotal = a + b
    return subtotal + (subtotal * 0.18)

# 2. Calculate reference book fines with 13% handling fee
def calculateReferenceFine(c, d):
    subtotal = c + d
    return subtotal + (subtotal * 0.13)

# 3. Calculate membership fee with 7% service tax
def calculateMembershipFee(e):
    return e + (e * 0.07)

# 4. Total dues combining all methods
def totalLibraryDues(a, b, c, d, e):
    late_fine_total = calculateLateBookFine(a, b)
    ref_fine_total = calculateReferenceFine(c, d)
    membership_total = calculateMembershipFee(e)
    
    return late_fine_total + ref_fine_total + membership_total

# 5. Calculate final payable amount after a 20% discount
def calculateDiscountedDues(a, b, c, d, e):
    total = totalLibraryDues(a, b, c, d, e)
    discount = total * 0.20
    return total - discount

# Test execution
if __name__ == "__main__":
    a, b, c, d, e = 100, 100, 100, 100, 100
    
    late_fine = calculateLateBookFine(a, b)
    ref_fine = calculateReferenceFine(c, d)
    member_fee = calculateMembershipFee(e)
    total_dues = totalLibraryDues(a, b, c, d, e)
    discount_amount = total_dues * 0.20
    final_payable = calculateDiscountedDues(a, b, c, d, e)
    
    print("--- Library Management System Calculation ---")
    print(f"Late Book Fine: {late_fine:.2f}")
    print(f"Reference Fine: {ref_fine:.2f}")
    print(f"Membership Fee: {member_fee:.2f}")
    print("-" * 45)
    print(f"Total after Dues = {total_dues:.2f} | Discount = ₹{discount_amount:.2f} | Final payable amount = {final_payable:.2f}")