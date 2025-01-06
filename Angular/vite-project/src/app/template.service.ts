import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

//Bjørn

@Injectable({
  providedIn: 'root'
})
export class TemplateService {
  private apiUrl = 'http://127.0.0.1:8000/insert-dynamic-data/';

  constructor(private http: HttpClient) {
  }
  
    sendDynamicData(templateFile: File, formData: any, apiKey: string): Observable<Blob> {
      const form = new FormData();
      form.append('templateFile', templateFile);
      form.append('contextFile', new Blob([JSON.stringify(formData)], { type: 'application/json' }));
  
      const headers = new HttpHeaders({
        'X-API-KEY': apiKey
        
      });
      console.log(headers, apiKey);
      return this.http.post(this.apiUrl, form, { headers, responseType: 'blob' });
      
  }
}