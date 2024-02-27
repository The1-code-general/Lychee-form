from flask import Flask, render_template, request
import smtplib
import os

app = Flask(__name__)

def generate_client_data(field_prefix, request_form):
    client_data = []
    index = 1
    while True:
        client_name = request_form.get(f'{field_prefix}_client_name_{index}')
        if client_name:
            product = request_form.get(f'{field_prefix}_product_{index}')
            prior_activities = request_form.get(f'{field_prefix}_prior_activities_{index}')
            present_activities = request_form.get(f'{field_prefix}_present_activities_{index}')
            outstanding_tasks = request_form.get(f'{field_prefix}_outstanding_tasks_{index}')
            
            client_info = {
                'Client Name': client_name,
                'Product': product,
                'Prior Activities': prior_activities,
                'Present Activities': present_activities,
                'Outstanding Tasks': outstanding_tasks
            }
            client_data.append(client_info)
            index += 1
        else:
            break
    return client_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    
    # Get the recipient's email address from the form
    recipient_email = request.form.get('recipient_email')
    
    # Check if recipient_email is not None and is not an empty string
    if recipient_email is not None and recipient_email.strip() != "":
        subject = 'Weekly Report'
                
        # Specify the URL of the image you want to include in the email
        image_address = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAQEhAQEBAVEBAVFxUbEBUWGRAQEA8SIBcaGyAXGBgaHigkHSAoIBkZJDIkJiotMC8wGx8zODM4NzQ5Li0BCgoKDg0OGBAQGi0dIB8xNzctNystKy0tNys3LystKy0zKystMS03NTc3NS81NTEvKy03Ny0tNzcrLTctNys3Lf/AABEIAMgAyAMBIgACEQEDEQH/xAAcAAEAAwEBAQEBAAAAAAAAAAAABQYHBAMBAgj/xABAEAABAwIDBAUJBQcFAQAAAAABAAIDBBEFEiEGMUFRBxMiYXEyNGJzgZGhsbIUI1JywSQlkrPR4fAVM0KEwhf/xAAaAQEAAgMBAAAAAAAAAAAAAAAABQYBAgME/8QAKhEAAgIBAgYABgMBAAAAAAAAAAECAwQFERITITFBUSJhcbHB8CMyYgb/2gAMAwEAAhEDEQA/ANxREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQHxFF43jtPRtzzvDb+S0avf4BUifpOeXEQ0oyc3uOY+4aLjZkV19JM7149li3iuhpaKl4Rt22XR8OVw8oTOb3XsrRQYjFOLsdfmNxC0ry6pvZS6msqZxW7XQ7URF6TkEReDahpe6IHtta1zhr5JJA+koD3REQBERAEREAREQBERAEREAREQBERAfFAbW7Sx0MWY9qZ1+qZzPM8gFJ4riEdNE+aQ2a0X7yeAHeVhmLYjLXTulkOp3DW0bODQvHl5HKjsu7Pbh4ytblL+qPOqqZauR0szy5x3k8O4cgv0QGjkAvQgNHIBRNVUF55DgFFVVyulu+wz85RXDHt4R20WIlssZGjcwDu8HRaBhdQY5G2NgdCssBtY8eC0hh1BXDVKFXGLXTc6aXzJ1z5nZ9i+02I2Ia/joD396lAVV6kXY7wuurAcVDrQvPat2D+IDh4rfRNTlb/DY934Z4r0oT29k+ouDzyf1MH1yqUUXB53P6mD65VZTQlEREMBERAEREAREQBERAEREAREQHxEUVtPiopKaWY7wLMHN50A961lJRW7NoxcmkvJnXSfj3XTCljP3cR7dv+Uv9vndV2lgyN7zvXNRMMj3SONzclxP/JxXXXS5W6bzoFX7JSut+pLZVkcelVrx3I3Eqi5yjcN/eVxd/uXqWrxcpzFxkvoiv48HkWOcux+qVmZ7Bzc0fFaFDJcgcys5wqbPVMY3cy7nnw3D32WgYP25o2+kD7tVFa605JekWnFhw1uRdptGO/KfkqjiFS6NrZGGz2Oa5pVqxF+WKQ+iVSsSf90R4fNV/RIt3xf+iuajL4kaphVa2eGOZu57QfA8R714Qedzeph+uZVjozxG7ZacnybOZ+U6H4/NWeDzuf1MP1yq+PuzfhaS38o6KnEYI3Bkk0bHHc1zmNcR3AldSxLpiH70pPVQ/wA562wI0ZlHZI/SIvl1g1C5YMRge4xsmjfIL3a17HPFt9wDddSw/oyH78q/+z/MCylubxjum/RuKIiwaBERAEREAREQHxZj0uYld0NM0+SC947zo39fetNcVhOM1Jqq6aQ6gvNvyN0HwC8OfZw17eyQ06Cdjm+0T9UUORgHE6nxUdWvzOPIaBS1W/K089wUM/S5Xn06ni3mRWq5DnYq15/Ucs3L3qNudVXNg6rtUuRXUW07z3zUo/eqUtv6rTrmnAyaPbFRo6fFLPz9nl7nRYhqYZWMyx81JrqXIUio0AEk8R9/VH3rWYiFqJs2ZgxXXekpUqqmpmZpUJpZUVtO6Cdh/dQTTuVweWnHBpUxRz0AmqE8skZm4VBUyOg74FpOTJ6nkM/U+8tXX8F2xhc+kdBzPlWUVL3qVu3c0FSSBncM8u43TBI6EgzwMYFLkGlcXau8Ob6sFwvWotFUGzHvNEALrHcAdyXnukZ5fzo6m9UA5z1DNXI5KnN3X8Sjt2atGhrPm5NSCfUGnuhnhL60e7LlSn9T1U1VB1U/dPyRpF6rXJ9rbywN5ZYxwThnZk1xXC+a9Go3doD6zatBItUEN0RqFS6ksxL8vMk0qCdwQdO3WjFZyq6Tm+LrZ1OWFkkSNnm3TaN6Hp0VYJNUcfsFRI9zkdW9yytXoFZznuHfPTc0kk/vqA8u1hnFluVnMTqWjsMUzRJO4/dQyynG6xEsMlTKk8S4I3t1Htu6jIbxbjR25ApuNLsWfT6V7WnlEaw3rNe23nYbU2HlqB6/A1LfdzkcXanZnFXFsLHl8T3fp2Iz/mvmvp8CpCtY60gZmBAAxkgC/ZC1uN2qI5I9sVFnDNeIz1vhnjjnRjZ46RxH1prvY2zyD30OTwpqq9WMjzy6cXK6hq+gDzrmk+iqGoTcawbPuPYlZWp0u7sLjccm5EH2o6nbWnbLSxHlre7GD/wAJFNBb7jnVzK43F1oI+qQdwqEnHPUZ7i/mz/wBOy4ObVlRsK0mrYhoqBlBxx8fKor6x+EAd8yVbS9JrRUwJBHHI/h9vbNjUfhs7msbR7nJ3UsxY/3jHl+ouStUElUSSTzjpXLdyc0APj2rmqRlz8lPtzU9p+5/iKzgBw0h+lb86m9VD9cqkV6epnpUq7EgDI8kClyZtk4vDXvnu4/WlJqmVmJ6ZTkNpHS5zx6m9VD9cqkt63uVIzqVeCVYkaYAfOal6zupG2Q6jiqqGgDl6VNLNqBmmmmFIBdmCqnigwB3Hagp0bbGKmiiaY/0ouQQfihKnQAme6jXtXZsra/p3sPw8MVmlrz3chwdHqfaVKBik5J6CiszkZA9qFzGQgknbzXunDWu23ZuzrcPuoVTumUbcnOQexouJrJ5bk1Bcdtv0ztqAHTscEjfU+0Rz9RqQMSMY68Aemad9Jjttt8ds+oJF1w9vtuXUj/wAtqxxhjEx66VFZVcyoHDFwnoapIbiVIbQ8Lcbst1pmn6/hm33GQRo2C0gXtxyCQaAPrVY0wIxD0P51rQ2KKKKkH/2Q=="

        
        # Create the email body with the form data formatted as an HTML table
        body = f'<html><body style="background-color: #f4f4f4; padding: 20px; font-family: Arial, sans-serif;">'
        body += f'<img src="{image_address}" alt="Weekly Report Image" style="width: 100%; max-width: 600px; margin-bottom: 20px;">'
        body += f'<h2 style="text-align: center;">Lychee Integrated Solutions Weekly Report</h2>'
        body += f'<p>Thank you, {name}, for submitting your weekly report.</p>'
        
        sections = [
            ('Support', 'support'),
            ('Implementation', 'implementation'),
            ('Reimplementation/Rescue', 'reimplementation_rescue')
        ]

        # Iterate through sections and add section name above each section
        for section_name, field_prefix in sections:
            client_data = generate_client_data(field_prefix, request.form)
            
            # Check if there is data for this section
            if client_data:
                body += f'<div style="margin-top: 20px;"><b>{section_name} Section</b></div>'
                
                # Add client data to the email body in a horizontal table format
                body += '<table style="width: 100%; border-collapse: collapse; margin-top: 10px;">'
                # Add table header row
                body += '<tr><th style="border: 1px solid black; padding: 8px;">Client Name</th>'
                body += '<th style="border: 1px solid black; padding: 8px;">Product</th>'
                body += '<th style="border: 1px solid black; padding: 8px;">Prior Activities</th>'
                body += '<th style="border: 1px solid black; padding: 8px;">Present Activities</th>'
                body += '<th style="border: 1px solid black; padding: 8px;">Outstanding Tasks</th></tr>'
                
                # Add client data rows
                for client in client_data:
                    body += '<tr>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Client Name"]}</td>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Product"]}</td>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Prior Activities"]}</td>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Present Activities"]}</td>'
                    body += f'<td style="border: 1px solid black; padding: 8px;">{client["Outstanding Tasks"]}</td>'
                    body += '</tr>'
                
                body += '</table>'
        
        body += f'<p><b>Recipient Email:</b> {recipient_email}</p>'
        body += '</body></html>'
        
        try:
            # Use environment variables for secure configuration
            smtp_server = os.environ.get('SMTP_SERVER')
            smtp_port = os.environ.get('SMTP_PORT')
            sender_email = os.environ.get('SENDER_EMAIL')
            sender_password = os.environ.get('SENDER_PASSWORD')

            # Send the email with HTML content
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('emmapharez29@gmail.com', 'kyea qryp pqfg wrvj')
            
            # Set the content type to HTML
            msg = f'Subject: {subject}\n'
            msg += 'MIME-Version: 1.0\n'
            msg += 'Content-type: text/html\n\n'
            msg += body
            
            server.sendmail('emmapharez29@gmail.com', recipient_email, msg)
            server.quit()
            
            # Render the success page with the provided name
            return render_template('success.html', name=name)
        except smtplib.SMTPConnectError as e:
            return f'Error connecting to SMTP server: {str(e)}'
        except smtplib.SMTPAuthenticationError as e:
            return f'Error authenticating with SMTP server: {str(e)}'
        except smtplib.SMTPException as e:
            return f'SMTP error: {str(e)}'
        except Exception as e:
            return f'An unexpected error occurred: {str(e)}'
    else:
        return "Recipient's email address is missing or invalid"

if __name__ == '__main__':
    app.run(debug=True, port=8080)
