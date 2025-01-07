function exportOrderDetails() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Set font styles
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);

    // Add company logo/header
    doc.text("Order Confirmation", 105, 20, { align: "center" });

    // Add success checkmark
    doc.setTextColor(25, 135, 84); // Bootstrap success color
    doc.text("✓", 105, 35, { align: "center" });

    // Reset text color and font for content
    doc.setTextColor(33, 37, 41);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(12);

    // Add thank you message
    doc.text("Thank you for your purchase!", 105, 50, { align: "center" });

    // Add separator line
    doc.setLineWidth(0.5);
    doc.line(20, 60, 190, 60);

    // Order details section
    doc.setFont("helvetica", "bold");
    doc.text("Order Details", 20, 75);
    doc.setFont("helvetica", "normal");

    const orderDetails = {
        orderNumber: document.getElementById('orderNumber').textContent,
        orderDate: document.getElementById('orderDate').textContent,
        totalAmount: document.getElementById('orderAmount').textContent
    };

    // Add order information
    doc.text(`Order Number: ${orderDetails.orderNumber}`, 20, 90);
    doc.text(`Date: ${orderDetails.orderDate}`, 20, 100);
    doc.text(`Total Amount: {{ total_cost }} rub.`, 20, 110);

    // Add footer
    doc.setFontSize(10);
    doc.text("This is an automatically generated document.", 105, 270, { align: "center" });

    // Save the PDF
    doc.save('order-details.pdf');
}