import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TypeInfoComponent } from './type-info.component';

describe('TypeInfoComponent', () => {
  let component: TypeInfoComponent;
  let fixture: ComponentFixture<TypeInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TypeInfoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TypeInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
