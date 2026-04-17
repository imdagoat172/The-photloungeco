import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-contact',
  imports: [FormsModule],
  templateUrl: './contact.html',
  styleUrl: './contact.css',
})
export class Contact {
  inquiry = {
    name: '',
    email: '',
    phone: '',
    eventType: '',
    message: ''
  };

  constructor(private http: HttpClient) {}

  onSubmit() {
    this.http.post('http://localhost:5000/api/inquiry', this.inquiry).subscribe(
      response => {
        alert('Inquiry submitted successfully!');
        this.inquiry = { name: '', email: '', phone: '', eventType: '', message: '' };
      },
      error => {
        alert('Error submitting inquiry.');
      }
    );
  }
}
