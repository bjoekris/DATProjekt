import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { jsPDF } from 'jspdf';

@Component({
  selector: 'app-invoice',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './invoice.component.html',
  styleUrl: './invoice.component.css'
})
export class InvoiceComponent {
  invoiceData = {
    customerName: '',
    dueDate: '',
    items: [
      {
        description: '',
        quantity: 0,
        price: 0,
      }
    ],
  }

  addItem() {
    this.invoiceData.items.push({
      description: '',
      quantity: 1,
      price: 0,
    });
  }

  removeItem(index: number) {
    this.invoiceData.items.splice(index, 1);
  }

  calculateTotal() {
    return this.invoiceData.items.reduce(
      (total, item) => total + item.quantity * item.price,
      0
    );
  }


  generateInvoice(form: any) {
    const doc = new jsPDF();

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(20);
    doc.text('Invoice', 10, 10);

    doc.setFontSize(12);
    doc.setFont('helvetica', 'normal');
    doc.text('Customer Name:' + this.invoiceData.customerName, 10, 20);
    doc.text('Due Date:' + this.invoiceData.dueDate, 10, 40);
    doc.text('Issue Date:' + new Date().toDateString(), 10, 50);

    doc.text('Description', 10, 60);
    doc.text('Quantity', 100, 60);
    doc.text('Price', 130, 60);
    doc.text('Total', 160, 60);


    let y = 70;
    this.invoiceData.items.forEach((item) => {
      doc.text(item.description, 10, y);
      doc.text(item.quantity.toString(), 100, y);
      doc.text(item.price.toFixed(2), 130, y);
      doc.text((item.quantity * item.price).toFixed(2), 160, y);
      y += 10;
    });

    doc.text('Total', 130, y);
    doc.text(this.calculateTotal().toFixed(2), 160, y);

    const pdfBlob= doc.output('blob');
    const blobUrl = URL.createObjectURL(pdfBlob);
    window.open(blobUrl);
  }
}

