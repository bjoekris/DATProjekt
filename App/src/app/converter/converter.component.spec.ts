import { TestBed } from '@angular/core/testing';
import { ConverterComponent } from './converter.component';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConverterComponent],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(ConverterComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have the 'vite-project' title`, () => {
    const fixture = TestBed.createComponent(ConverterComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('vite-project');
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(ConverterComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Hello, vite-project');
  });
});
