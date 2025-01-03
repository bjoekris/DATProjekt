import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

import { saveAs } from 'file-saver';
import { TemplateService } from './template.service';
import mammoth from 'mammoth';

interface DynamicField {
  name: string;
  type: 'text' | 'number' | 'file' | 'media' | 'repeat';
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [HttpClient]
})
export class AppComponent {
  templateFile: File | null = null;
  formData: any = {};
  dynamicFields: DynamicField[] = [];
  title = 'App';

  constructor(private templateService: TemplateService, private http: HttpClient) {}

  async onFileChange(event: any): Promise<void> {
    this.templateFile = event.target.files[0];
    console.log("OnFileChange function called");
    const file = event.target.files[0];

    try {
      const arrayBuffer = await file.arrayBuffer();
      const result = await mammoth.extractRawText({ arrayBuffer });
      const text = result.value;

      const regex = /{{([^}]+)}}/g;
      const matches = text.matchAll(regex);

      this.dynamicFields = [];
      for (const match of matches) {
        const variable = match[1].trim();
        let type: DynamicField['type'] = 'text';
        if (variable.endsWith('_text')) {
          type = 'text';
        } else if (variable.endsWith('_number')) {
          type = 'number';
        } else if (variable.endsWith('_file')) {
          type = 'file';
        } else if (variable.endsWith('media')) {
          type = 'media';
        } else if (variable.endsWith('_repeat')) {
          type = 'repeat';
        }
       //Repeat function til at gentage felter

        const name = variable.replace(/(?:text|number|file|media)$/, '');
        this.dynamicFields.push({ name, type });
      }

      console.log("DynamicFields:", this.dynamicFields);
    } catch (error) {
      console.error("Error processing DOCX file:", error);
    }
  }

  onSubmit() {
    console.log("OnSubmit function called");
    if (!this.templateFile) {
      alert('Please upload a template file.');
      return;
    }

    const apiKey = 'abc123456789';
    this.templateService.sendDynamicData(this.templateFile, this.formData, apiKey)
      .subscribe(response => {
        saveAs(response, 'generated.pdf');
      }, error => {
        console.error('Error generating PDF:', error);
      });
  }
}