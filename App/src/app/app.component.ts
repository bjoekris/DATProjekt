import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  templateFile: File | null = null;
  formData: any = {};
  dynamicFields: string[] = []; // Add this line to define dynamicFields
  title = 'App';

  constructor(private http: HttpClient) {}

  onFileChange(event: any) {
    this.templateFile = event.target.files[0];
  }

  onSubmit() {
    if (!this.templateFile) {
      alert('Please upload a template file.');
      return;
    }

    const formData = new FormData();
    formData.append('templateFile', this.templateFile);
    formData.append('contextFile', new Blob([JSON.stringify(this.formData)], { type: 'application/json' }));

    const headers = new HttpHeaders({
      'x-api-key': 'your-api-key-here'
    });

    this.http.post('/insert-dynamic-data/', formData, { headers, responseType: 'blob' })
      .subscribe(response => {
        saveAs(response, 'generated.pdf');
      }, error => {
        console.error('Error generating PDF:', error);
      });
  }
}