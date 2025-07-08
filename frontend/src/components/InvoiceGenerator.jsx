import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import {
  Box,
  Button,
  Field,
  Input,
  Select,
  VStack,
  HStack,
  Text,
  Heading,
  Separator,
} from '@chakra-ui/react';

const InvoiceGenerator = () => {
  const { orderId } = useParams();
  const [discountType, setDiscountType] = useState('percent');
  const [discountValue, setDiscountValue] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  
  // Simple notification function using browser alert
  const showNotification = (title, message, type) => {
    alert(`${title}: ${message}`);
  };

  const handleDiscountTypeChange = (e) => {
    setDiscountType(e.target.value);
  };

  const handleDiscountValueChange = (e) => {
    setDiscountValue(e.target.value);
  };

  const generateInvoice = async (withDiscount = false) => {
    setIsLoading(true);
    try {
      let url = `/seller/invoices/${orderId}`;
      
      if (withDiscount) {
        url = `/seller/invoices/${orderId}/with-discount?discount_type=${discountType}&discount_value=${discountValue}`;
      }
      
      const response = await axios.get(url, {
        responseType: 'blob',
      });
      
      // Create a blob from the PDF Stream
      const file = new Blob([response.data], { type: 'application/pdf' });
      
      // Build a URL from the file
      const fileURL = URL.createObjectURL(file);
      
      // Open the URL on new Window
      const pdfWindow = window.open();
      pdfWindow.location.href = fileURL;
      
      showNotification(
        'Invoice generated',
        'The invoice has been generated successfully.',
        'success'
      );
    } catch (error) {
      console.error('Error generating invoice:', error);
      showNotification(
        'Error',
        'Failed to generate invoice. Please try again.',
        'error'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box p={5} shadow="md" borderWidth="1px" borderRadius="md">
      <Heading size="md" mb={4}>Generate Invoice</Heading>
      <Separator mb={4} />
      
      <VStack spacing={4} align="stretch">
        <Button
          colorScheme="blue"
          isLoading={isLoading}
          onClick={() => generateInvoice(false)}
          width="full"
        >
          Generate Standard Invoice
        </Button>
        
        <Text fontWeight="bold" mt={4}>Apply Discount</Text>
        
        <Field.Root>
          <Field.Label>Discount Type</Field.Label>
          <Select value={discountType} onChange={handleDiscountTypeChange}>
            <option value="percent">Percentage (%)</option>
            <option value="amount">Fixed Amount ($)</option>
          </Select>
        </Field.Root>
        
        <Field.Root>
          <Field.Label>
            {discountType === 'percent' ? 'Discount Percentage' : 'Discount Amount'}
          </Field.Label>
          <Input
            type="number"
            value={discountValue}
            onChange={handleDiscountValueChange}
            min="0"
            max={discountType === 'percent' ? '100' : undefined}
            step="0.01"
          />
        </Field.Root>
        
        <Button
          colorScheme="green"
          isLoading={isLoading}
          onClick={() => generateInvoice(true)}
          width="full"
          mt={2}
        >
          Generate Invoice with Discount
        </Button>
      </VStack>
    </Box>
  );
};

export default InvoiceGenerator;