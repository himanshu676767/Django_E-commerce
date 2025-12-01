# utils.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def generate_invoice(order, save_to_file=False):
	buffer = BytesIO()
	p = canvas.Canvas(buffer, pagesize=letter)

	x, y = 50, 750

	# Header
	p.setFont("Helvetica-Bold", 16)
	p.drawString(x, y, f"Invoice for Order #{order.id}")
	y -= 30

	p.setFont("Helvetica", 12)
	invoice_date = datetime.today().strftime("%d-%b-%Y")
	due_date = (datetime.today() + timedelta(days=7)).strftime("%d-%b-%Y")
	p.drawString(x, y, f"Invoice Date: {invoice_date}")
	y -= 20
	p.drawString(x, y, f"Due Date: {due_date}")
	y -= 30

	# Customer Details
	p.setFont("Helvetica-Bold", 12)
	p.drawString(x, y, "Customer Details:")
	y -= 20
	p.setFont("Helvetica", 12)
	p.drawString(x, y, f"Name: {order.user.username}")
	y -= 20
	p.drawString(x, y, f"Email: {order.user.email}")
	y -= 20
	phone = getattr(order.user, "phone", "N/A")
	p.drawString(x, y, f"Phone: {phone}")
	y -= 30

	# Items Table
	p.setFont("Helvetica-Bold", 12)
	p.drawString(x, y, "Items:")
	y -= 20
	p.setFont("Helvetica-Bold", 10)
	p.drawString(x, y, "Product")
	p.drawString(x + 200, y, "Qty")
	p.drawString(x + 250, y, "Unit Price")
	p.drawString(x + 350, y, "Total")
	y -= 15
	p.setFont("Helvetica", 10)
	p.line(x, y, x + 450, y)
	y -= 15

	subtotal = 0
	for item in order.items.all():
		total = item.quantity * item.price
		subtotal += total
		p.drawString(x, y, str(item.product.name))
		p.drawString(x + 200, y, str(item.quantity))
		p.drawString(x + 250, y, f"{item.price:.2f}")
		p.drawString(x + 350, y, f"{total:.2f}")
		y -= 20

	y -= 10
	tax = subtotal * 0.18  # 18% GST example
	grand_total = subtotal + tax

	p.setFont("Helvetica-Bold", 12)
	p.drawString(x, y, f"Subtotal: {subtotal:.2f}")
	y -= 20
	p.drawString(x, y, f"Tax (18% GST): {tax:.2f}")
	y -= 20
	p.drawString(x, y, f"Grand Total: {grand_total:.2f}")
	y -= 40

	# Payment Details
	p.setFont("Helvetica-Bold", 12)
	p.drawString(x, y, "Payment Details:")
	y -= 20
	p.setFont("Helvetica", 12)
	p.drawString(x, y, "Bank: STATE BANK OF INDIA")
	y -= 20
	p.drawString(x, y, "Account No: 17003976578123")
	y -= 20
	p.drawString(x, y, "UPI/Paytm ID: 7742443956@bank")
	y -= 30

	# Notes
	p.setFont("Helvetica-Bold", 12)
	p.drawString(x, y, "Notes:")
	y -= 20
	p.setFont("Helvetica", 12)
	p.drawString(x, y, "Please contact support@example.com for any queries.")
	y -= 30
	p.drawString(x, y, "Thank you for your business!")

	p.showPage()
	p.save()
	buffer.seek(0)

	file_path = None
	if save_to_file:
		folder = "media/invoices"
		os.makedirs(folder, exist_ok=True)
		file_path = f"{folder}/invoice_{order.id}.pdf"
		with open(file_path, "wb") as f:
			f.write(buffer.getvalue())

	return buffer, file_path


def get_order_totals(order):
	items_data = []
	subtotal = 0
	for item in order.items.all():
		total = item.quantity * item.price
		subtotal += total
		items_data.append({
			'product': item.product,
			'quantity': item.quantity,
			'price': item.price,
			'total': total
		})
	tax = subtotal * 0.18  # 18% GST
	grand_total = subtotal + tax
	return items_data, subtotal, tax, grand_total

def send_invoice_email(order):
	pdf_buffer, file_path = generate_invoice(order, save_to_file=True)
	items_data, subtotal, tax, grand_total = get_order_totals(order)

	context = {
		'order': order,
		'items': items_data,
		'subtotal': subtotal,
		'tax': tax,
		'grand_total': grand_total
	}

	message = render_to_string('emails/invoice_email.html', context)
	email = EmailMessage(
		subject=f"Invoice for Order #{order.id}",
		body=message,
		to=[order.user.email]
	)
	email.attach(f"invoice_{order.id}.pdf", pdf_buffer.getvalue(), 'application/pdf')
	email.content_subtype = 'html'
	email.send()
