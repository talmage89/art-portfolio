import * as React from 'react';
import { ArrowLeftIcon } from 'lucide-react';
import { CheckoutFooter } from '..';
import './CheckoutForm.scss';

type CheckoutFormProps = {
  createSessionLoading: boolean;
  onBack: () => void;
  onSubmit: (data: CheckoutFormData) => void;
};

export type CheckoutFormData = {
  name: string;
  email: string;
  street1: string;
  street2?: string;
  city: string;
  state: string;
  postalCode: string;
  country?: string;
};

export const CheckoutForm = (props: CheckoutFormProps) => {
  const [formData, setFormData] = React.useState<CheckoutFormData>({
    name: '',
    email: '',
    street1: '',
    city: '',
    state: '',
    postalCode: '',
  });

  const [formDataErrors, setFormDataErrors] = React.useState<Partial<CheckoutFormData>>({});

  function validateData() {
    const errors: Partial<CheckoutFormData> = {};
    if (!formData.name) errors.name = 'Name is required';
    if (!formData.email) errors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) errors.email = 'Please enter a valid email address';
    if (!formData.street1) errors.street1 = 'Street address is required';
    if (!formData.city) errors.city = 'City is required';
    if (!formData.state) errors.state = 'State is required';
    if (!formData.postalCode) errors.postalCode = 'Postal code is required';
    else if (!/^\d{5}(-\d{4})?$/.test(formData.postalCode)) errors.postalCode = 'Please enter a valid postal code';

    setFormDataErrors(errors);
    return Object.keys(errors).length === 0;
  }

  const renderFormGroup = ({
    id,
    label,
    required = false,
    placeholder,
    type = 'text',
    value,
    onChange,
    error,
  }: {
    id: keyof CheckoutFormData;
    label: string;
    required?: boolean;
    placeholder: string;
    type?: string;
    value: string | undefined;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    error?: string;
  }) => (
    <div className={`CheckoutForm__form__group${error ? ' error' : ''}`}>
      <label className="CheckoutForm__form__label" htmlFor={id}>
        {label}
        {required && <span className="CheckoutForm__form__label__required">*</span>}
      </label>
      <input
        className="CheckoutForm__form__input"
        type={type}
        id={id}
        name={id}
        placeholder={placeholder}
        value={value || ''}
        onChange={(e) => {
          onChange(e);
          error && setFormDataErrors((p) => ({ ...p, [id]: undefined }));
        }}
      />
      {error && <span className="CheckoutForm__form__error">{error}</span>}
    </div>
  );

  return (
    <div className="CheckoutForm">
      <form className="CheckoutForm__form">
        <div className="CheckoutForm__form__header">
          <button className="CheckoutForm__form__header__back" onClick={props.onBack}>
            <ArrowLeftIcon />
          </button>
          <h2>Shipping Information</h2>
        </div>
        {renderFormGroup({
          id: 'name',
          label: 'Name',
          required: true,
          type: 'text',
          placeholder: 'Your Name',
          value: formData.name,
          onChange: (e) => setFormData((p) => ({ ...p, name: e.target.value })),
          error: formDataErrors.name,
        })}
        {renderFormGroup({
          id: 'email',
          label: 'Email Address',
          required: true,
          type: 'email',
          placeholder: 'example@email.com',
          value: formData.email,
          onChange: (e) => setFormData((p) => ({ ...p, email: e.target.value })),
          error: formDataErrors.email,
        })}
        {renderFormGroup({
          id: 'street1',
          label: 'Street Address',
          required: true,
          placeholder: '123 Main St',
          value: formData.street1,
          onChange: (e) => setFormData((p) => ({ ...p, street1: e.target.value })),
          error: formDataErrors.street1,
        })}
        {renderFormGroup({
          id: 'street2',
          label: 'Street Address Line 2 (optional)',
          placeholder: 'Apt, Suite, Unit, etc.',
          value: formData.street2,
          onChange: (e) => setFormData((p) => ({ ...p, street2: e.target.value })),
        })}
        <div className="CheckoutForm__form__row">
          {renderFormGroup({
            id: 'city',
            label: 'City',
            required: true,
            placeholder: 'New York',
            value: formData.city,
            onChange: (e) => setFormData((p) => ({ ...p, city: e.target.value })),
            error: formDataErrors.city,
          })}
          <div className="CheckoutForm__form__row">
            {renderFormGroup({
              id: 'state',
              label: 'State/Province/Region',
              required: true,
              placeholder: 'NY',
              value: formData.state,
              onChange: (e) => setFormData((p) => ({ ...p, state: e.target.value })),
              error: formDataErrors.state,
            })}
            {renderFormGroup({
              id: 'postalCode',
              label: 'Postal Code',
              required: true,
              placeholder: '10001',
              value: formData.postalCode,
              onChange: (e) => setFormData((p) => ({ ...p, postalCode: e.target.value })),
              error: formDataErrors.postalCode,
            })}
            {renderFormGroup({
              id: 'country',
              label: 'Country',
              placeholder: 'United States',
              value: formData.country,
              onChange: (e) => setFormData((p) => ({ ...p, country: e.target.value })),
              error: formDataErrors.country,
            })}
          </div>
        </div>
      </form>
      <CheckoutFooter
        disabled={
          !formData.name ||
          !formData.email ||
          !formData.street1 ||
          !formData.city ||
          !formData.state ||
          !formData.postalCode
        }
        loading={props.createSessionLoading}
        text="Proceed to Payment"
        onClick={() => {
          validateData() && props.onSubmit(formData);
        }}
      />
    </div>
  );
};
