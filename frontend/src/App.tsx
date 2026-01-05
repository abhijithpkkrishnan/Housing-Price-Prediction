import { useState, useRef, useEffect } from 'react';

interface FormData {
  area: number;
  bedrooms: number;
  bathrooms: number;
  stories: number;
  mainroad: string;
  guestroom: string;
  basement: string;
  hotwaterheating: string;
  airconditioning: string;
  parking: number;
  prefarea: string;
  furnishingstatus: string;
}

const initialFormData: FormData = {
  area: 4000,
  bedrooms: 3,
  bathrooms: 2,
  stories: 2,
  mainroad: "yes",
  guestroom: "no",
  basement: "no",
  hotwaterheating: "no",
  airconditioning: "yes",
  parking: 1,
  prefarea: "no",
  furnishingstatus: "furnished"
};

// Custom Select Component for better styling
const CustomSelect = ({ 
  label, 
  name, 
  value, 
  options, 
  onChange 
}: { 
  label: string, 
  name: string, 
  value: string, 
  options: string[], 
  onChange: (name: string, value: string) => void 
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="flex flex-col gap-3 group relative" ref={dropdownRef}>
      <label className="text-sm font-medium text-blue-300 ml-2 tracking-wide uppercase text-xs group-hover:text-blue-200 transition-colors">
        {label}
      </label>
      <div 
        onClick={() => setIsOpen(!isOpen)}
        className={`neumorphic-inset w-full p-4 text-white flex justify-between items-center cursor-pointer transition-all ${isOpen ? 'ring-2 ring-blue-500/30' : ''}`}
      >
        <span className="capitalize">{value}</span>
        <svg 
          className={`fill-current h-4 w-4 text-blue-300 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} 
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 20 20"
        >
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
        </svg>
      </div>
      
      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute z-10 top-[calc(100%+8px)] left-0 w-full bg-[#141b2d] rounded-xl shadow-[10px_10px_20px_#0b0f19,-10px_-10px_20px_#1d2741] border border-white/5 overflow-hidden animate-in fade-in zoom-in-95 duration-100">
          <div className="max-h-60 overflow-y-auto py-2 custom-scrollbar">
            {options.map((opt) => (
              <div
                key={opt}
                onClick={() => {
                  onChange(name, opt);
                  setIsOpen(false);
                }}
                className={`px-4 py-3 cursor-pointer capitalize transition-colors flex items-center justify-between
                  ${value === opt ? 'bg-blue-500/10 text-blue-400' : 'text-gray-300 hover:bg-white/5 hover:text-white'}
                `}
              >
                {opt}
                {value === opt && (
                  <svg className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                  </svg>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

function App() {
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'area' || name === 'bedrooms' || name === 'bathrooms' || name === 'stories' || name === 'parking' 
        ? Number(value) 
        : value
    }));
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Prediction failed');
      }

      const data = await response.json();
      setPrediction(data.predicted_price);
    } catch (err) {
      setError('Failed to get prediction. Ensure backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const InputField = ({ label, name, type = "text" }: { label: string, name: keyof FormData, type?: string }) => (
    <div className="flex flex-col gap-3 group">
      <label className="text-sm font-medium text-blue-300 ml-2 tracking-wide uppercase text-xs group-hover:text-blue-200 transition-colors">
        {label}
      </label>
      <input
        type={type}
        name={name}
        value={formData[name]}
        onChange={handleChange}
        className="neumorphic-inset w-full p-4 text-white outline-none focus:ring-0 transition-all placeholder-gray-600"
        placeholder={`Enter ${label.toLowerCase()}`}
      />
    </div>
  );

  return (
    <div className="min-h-screen flex items-center justify-center py-16 px-4 sm:px-6 lg:px-8 bg-[#141b2d]">
      <div className="max-w-5xl w-full space-y-12">
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-bold tracking-tight text-white bg-clip-text text-transparent bg-gradient-to-r from-blue-200 to-blue-500">
            Housing Price Prediction
          </h1>
          <p className="text-lg text-blue-200/60 max-w-2xl mx-auto">
            Leverage advanced machine learning to estimate market value with precision.
          </p>
        </div>

        <div className="neumorphic p-10 md:p-14 border border-white/5">
          <form onSubmit={handleSubmit} className="space-y-10">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-10">
              <InputField label="Area (sq ft)" name="area" type="number" />
              <InputField label="Bedrooms" name="bedrooms" type="number" />
              <InputField label="Bathrooms" name="bathrooms" type="number" />
              <InputField label="Stories" name="stories" type="number" />
              <InputField label="Parking Spots" name="parking" type="number" />
              
              <CustomSelect 
                label="Main Road" 
                name="mainroad" 
                value={formData.mainroad} 
                options={["yes", "no"]} 
                onChange={handleSelectChange} 
              />
              <CustomSelect 
                label="Guest Room" 
                name="guestroom" 
                value={formData.guestroom} 
                options={["yes", "no"]} 
                onChange={handleSelectChange} 
              />
              <CustomSelect 
                label="Basement" 
                name="basement" 
                value={formData.basement} 
                options={["yes", "no"]} 
                onChange={handleSelectChange} 
              />
              <CustomSelect 
                label="Hot Water Heating" 
                name="hotwaterheating" 
                value={formData.hotwaterheating} 
                options={["yes", "no"]} 
                onChange={handleSelectChange} 
              />
              <CustomSelect 
                label="Air Conditioning" 
                name="airconditioning" 
                value={formData.airconditioning} 
                options={["yes", "no"]} 
                onChange={handleSelectChange} 
              />
              <CustomSelect 
                label="Preferred Area" 
                name="prefarea" 
                value={formData.prefarea} 
                options={["yes", "no"]} 
                onChange={handleSelectChange} 
              />
              <CustomSelect 
                label="Furnishing Status" 
                name="furnishingstatus" 
                value={formData.furnishingstatus} 
                options={["furnished", "semi-furnished", "unfurnished"]} 
                onChange={handleSelectChange} 
              />
            </div>

            <div className="flex justify-center pt-8">
              <button
                type="submit"
                disabled={loading}
                className="neumorphic-btn px-16 py-5 text-xl font-bold text-blue-400 hover:text-blue-300 disabled:opacity-50 disabled:cursor-not-allowed w-full md:w-auto tracking-wide"
              >
                {loading ? (
                  <span className="flex items-center gap-3">
                    <svg className="animate-spin h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Calculating...
                  </span>
                ) : 'Predict Market Value'}
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-10 p-4 bg-red-900/20 border border-red-500/50 rounded-xl text-red-200 text-center animate-pulse">
              {error}
            </div>
          )}

          {prediction !== null && (
            <div className="mt-12 text-center animate-fade-in space-y-4">
              <div className="text-blue-200/60 uppercase tracking-widest text-sm font-semibold">Estimated Market Value</div>
              <div className="text-6xl font-bold text-green-400 neumorphic-inset inline-block px-12 py-6 rounded-2xl tracking-tight shadow-[0_0_30px_rgba(74,222,128,0.1)]">
                ${prediction.toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
