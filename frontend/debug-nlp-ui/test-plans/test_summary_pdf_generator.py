#!/usr/bin/env python3

"""
Test Summary PDF Generator

This script generates PDF test summary reports for the WhatsApp chatbot testing.
It can create daily and weekly reports based on test data stored in CSV or JSON format.

Usage:
    python test_summary_pdf_generator.py --type [daily|weekly] --date YYYY-MM-DD --output report.pdf

Requirements:
    - pandas
    - matplotlib
    - reportlab
    - argparse
    - json
    - csv
    - datetime
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import json
import csv
import argparse
import datetime
import os
import sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from io import BytesIO

# Default paths
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test-data')
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test-reports')

# Ensure output directory exists
if not os.path.exists(DEFAULT_OUTPUT_DIR):
    os.makedirs(DEFAULT_OUTPUT_DIR)

# Define color schemes
COLORS = {
    'primary': colors.HexColor('#1a73e8'),  # Google Blue
    'secondary': colors.HexColor('#fbbc04'),  # Google Yellow
    'success': colors.HexColor('#34a853'),  # Google Green
    'danger': colors.HexColor('#ea4335'),  # Google Red
    'light': colors.HexColor('#f8f9fa'),
    'dark': colors.HexColor('#202124'),
    'gray': colors.HexColor('#dadce0'),
    'hindi': colors.HexColor('#ff9800'),  # Orange for Hindi
    'hinglish': colors.HexColor('#9c27b0'),  # Purple for Hinglish
    'english': colors.HexColor('#2196f3'),  # Blue for English
}

# Define chart colors
CHART_COLORS = [COLORS['english'], COLORS['hindi'], COLORS['hinglish'], COLORS['secondary']]


class TestSummaryPDFGenerator:
    """Generate PDF test summary reports for WhatsApp chatbot testing."""

    def __init__(self, data_dir=DEFAULT_DATA_DIR, output_dir=DEFAULT_OUTPUT_DIR):
        """Initialize the PDF generator.

        Args:
            data_dir: Directory containing test data files
            output_dir: Directory to save generated PDF reports
        """
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom paragraph styles for the report."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=24,
            alignment=1,  # Center
            spaceAfter=20,
            textColor=COLORS['dark']
        ))

        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            alignment=1,  # Center
            spaceAfter=12,
            textColor=COLORS['primary']
        ))

        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6,
            textColor=COLORS['dark']
        ))

        # Normal text style
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=COLORS['dark']
        ))

        # Table header style
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=1,  # Center
            textColor=colors.white
        ))

    def _load_test_data(self, date_str, report_type='daily'):
        """Load test data for the specified date.

        Args:
            date_str: Date string in YYYY-MM-DD format
            report_type: 'daily' or 'weekly'

        Returns:
            Dictionary containing test data
        """
        # For weekly reports, calculate the date range
        if report_type == 'weekly':
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            # Assuming weeks start on Monday
            start_of_week = date_obj - datetime.timedelta(days=date_obj.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            date_range = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
            date_strs = [d.strftime('%Y-%m-%d') for d in date_range]
            
            # Load data for each day in the week
            combined_data = {
                'language_detection': [],
                'intent_recognition': [],
                'response_quality': [],
                'issues': [],
                'test_coverage': {'english': 0, 'hindi': 0, 'hinglish': 0},
                'command_success': {}
            }
            
            for day in date_strs:
                try:
                    day_data = self._load_daily_data(day)
                    for key in combined_data:
                        if key in ['language_detection', 'intent_recognition', 'response_quality', 'issues']:
                            combined_data[key].extend(day_data.get(key, []))
                        elif key == 'test_coverage':
                            for lang in combined_data[key]:
                                combined_data[key][lang] += day_data.get('test_coverage', {}).get(lang, 0)
                        elif key == 'command_success':
                            for cmd_type, success_rate in day_data.get('command_success', {}).items():
                                if cmd_type in combined_data[key]:
                                    combined_data[key][cmd_type] = (combined_data[key][cmd_type] + success_rate) / 2
                                else:
                                    combined_data[key][cmd_type] = success_rate
                except (FileNotFoundError, json.JSONDecodeError):
                    # Skip days with missing or invalid data
                    continue
            
            # Add date range information
            combined_data['date_range'] = {
                'start': start_of_week.strftime('%Y-%m-%d'),
                'end': end_of_week.strftime('%Y-%m-%d')
            }
            
            return combined_data
        else:
            # For daily reports
            return self._load_daily_data(date_str)

    def _load_daily_data(self, date_str):
        """Load test data for a specific day.

        Args:
            date_str: Date string in YYYY-MM-DD format

        Returns:
            Dictionary containing test data for the day
        """
        # Try to load from JSON first
        json_path = os.path.join(self.data_dir, f'test_data_{date_str}.json')
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                return json.load(f)
        
        # If JSON not found, try CSV
        csv_path = os.path.join(self.data_dir, f'test_data_{date_str}.csv')
        if os.path.exists(csv_path):
            return self._parse_csv_data(csv_path)
        
        # If no data found, use sample data for demonstration
        print(f"Warning: No data found for {date_str}, using sample data")
        return self._generate_sample_data(date_str)

    def _parse_csv_data(self, csv_path):
        """Parse test data from CSV file.

        Args:
            csv_path: Path to CSV file

        Returns:
            Dictionary containing parsed test data
        """
        # This is a simplified implementation
        # In a real scenario, you would parse the actual CSV structure
        data = {
            'language_detection': [],
            'intent_recognition': [],
            'response_quality': [],
            'issues': [],
            'test_coverage': {'english': 0, 'hindi': 0, 'hinglish': 0},
            'command_success': {}
        }
        
        try:
            df = pd.read_csv(csv_path)
            
            # Extract language detection data
            if 'language' in df.columns and 'detected_language' in df.columns:
                for _, row in df.iterrows():
                    data['language_detection'].append({
                        'actual': row['language'],
                        'detected': row['detected_language'],
                        'confidence': row.get('language_confidence', 0.0)
                    })
            
            # Extract intent recognition data
            if 'intent' in df.columns and 'detected_intent' in df.columns:
                for _, row in df.iterrows():
                    data['intent_recognition'].append({
                        'actual': row['intent'],
                        'detected': row['detected_intent'],
                        'confidence': row.get('intent_confidence', 0.0)
                    })
            
            # Extract response quality data
            if 'response_quality_score' in df.columns:
                for _, row in df.iterrows():
                    data['response_quality'].append({
                        'language': row.get('language', 'unknown'),
                        'score': row['response_quality_score'],
                        'command_type': row.get('command_type', 'unknown')
                    })
            
            # Extract test coverage
            for lang in data['test_coverage'].keys():
                data['test_coverage'][lang] = len(df[df['language'] == lang])
            
            # Extract command success rates
            if 'command_type' in df.columns and 'success' in df.columns:
                for cmd_type in df['command_type'].unique():
                    cmd_df = df[df['command_type'] == cmd_type]
                    if len(cmd_df) > 0:
                        success_rate = cmd_df['success'].mean() * 100
                        data['command_success'][cmd_type] = success_rate
            
            # Extract issues
            if 'issue_description' in df.columns:
                for _, row in df[df['issue_description'].notna()].iterrows():
                    data['issues'].append({
                        'description': row['issue_description'],
                        'severity': row.get('issue_severity', 'medium'),
                        'language': row.get('language', 'unknown'),
                        'command_type': row.get('command_type', 'unknown')
                    })
            
            return data
        
        except Exception as e:
            print(f"Error parsing CSV data: {e}")
            return self._generate_sample_data(os.path.basename(csv_path).split('_')[2].split('.')[0])

    def _generate_sample_data(self, date_str):
        """Generate sample test data for demonstration.

        Args:
            date_str: Date string in YYYY-MM-DD format

        Returns:
            Dictionary containing sample test data
        """
        # Sample language detection data
        language_detection = [
            {'actual': 'english', 'detected': 'english', 'confidence': 0.98},
            {'actual': 'english', 'detected': 'english', 'confidence': 0.97},
            {'actual': 'hindi', 'detected': 'hindi', 'confidence': 0.95},
            {'actual': 'hindi', 'detected': 'hindi', 'confidence': 0.94},
            {'actual': 'hinglish', 'detected': 'hinglish', 'confidence': 0.89},
            {'actual': 'hinglish', 'detected': 'hindi', 'confidence': 0.65},
            {'actual': 'english', 'detected': 'english', 'confidence': 0.99},
            {'actual': 'hindi', 'detected': 'hindi', 'confidence': 0.96},
            {'actual': 'hinglish', 'detected': 'hinglish', 'confidence': 0.88},
        ]
        
        # Sample intent recognition data
        intent_recognition = [
            {'actual': 'get_inventory', 'detected': 'get_inventory', 'confidence': 0.97},
            {'actual': 'get_orders', 'detected': 'get_orders', 'confidence': 0.96},
            {'actual': 'add_product', 'detected': 'add_product', 'confidence': 0.95},
            {'actual': 'get_report', 'detected': 'get_report', 'confidence': 0.93},
            {'actual': 'update_order', 'detected': 'update_order', 'confidence': 0.92},
            {'actual': 'get_customer', 'detected': 'get_orders', 'confidence': 0.68},
            {'actual': 'get_low_stock', 'detected': 'get_inventory', 'confidence': 0.72},
            {'actual': 'get_report', 'detected': 'get_report', 'confidence': 0.94},
            {'actual': 'add_product', 'detected': 'add_product', 'confidence': 0.96},
        ]
        
        # Sample response quality data
        response_quality = [
            {'language': 'english', 'score': 4.8, 'command_type': 'inventory'},
            {'language': 'english', 'score': 4.7, 'command_type': 'orders'},
            {'language': 'hindi', 'score': 4.2, 'command_type': 'inventory'},
            {'language': 'hindi', 'score': 4.0, 'command_type': 'orders'},
            {'language': 'hinglish', 'score': 3.9, 'command_type': 'inventory'},
            {'language': 'hinglish', 'score': 3.8, 'command_type': 'orders'},
            {'language': 'english', 'score': 4.6, 'command_type': 'reporting'},
            {'language': 'hindi', 'score': 4.1, 'command_type': 'reporting'},
            {'language': 'hinglish', 'score': 3.7, 'command_type': 'reporting'},
        ]
        
        # Sample issues
        issues = [
            {
                'description': 'Hinglish reporting commands below 80% success threshold',
                'severity': 'critical',
                'language': 'hinglish',
                'command_type': 'reporting'
            },
            {
                'description': 'Response time exceeding 3 seconds for complex Hindi queries',
                'severity': 'high',
                'language': 'hindi',
                'command_type': 'reporting'
            },
            {
                'description': 'Mixed language commands have low success rate',
                'severity': 'medium',
                'language': 'hinglish',
                'command_type': 'inventory'
            },
            {
                'description': 'Minor grammatical errors in responses',
                'severity': 'low',
                'language': 'hindi',
                'command_type': 'orders'
            },
        ]
        
        # Sample test coverage
        test_coverage = {
            'english': 50,
            'hindi': 40,
            'hinglish': 35
        }
        
        # Sample command success rates
        command_success = {
            'inventory': 92.5,
            'orders': 91.2,
            'reporting': 88.7,
            'customer': 90.1,
            'edge_cases': 82.3
        }
        
        return {
            'date': date_str,
            'language_detection': language_detection,
            'intent_recognition': intent_recognition,
            'response_quality': response_quality,
            'issues': issues,
            'test_coverage': test_coverage,
            'command_success': command_success
        }

    def _create_language_detection_chart(self, data):
        """Create a chart showing language detection accuracy.

        Args:
            data: Language detection data

        Returns:
            A ReportLab Drawing object containing the chart
        """
        # Calculate accuracy by language
        languages = ['english', 'hindi', 'hinglish']
        accuracy = {lang: {'correct': 0, 'total': 0} for lang in languages}
        
        for item in data:
            actual = item['actual']
            detected = item['detected']
            if actual in accuracy:
                accuracy[actual]['total'] += 1
                if actual == detected:
                    accuracy[actual]['correct'] += 1
        
        # Calculate percentages
        percentages = []
        for lang in languages:
            if accuracy[lang]['total'] > 0:
                pct = (accuracy[lang]['correct'] / accuracy[lang]['total']) * 100
            else:
                pct = 0
            percentages.append(pct)
        
        # Create drawing
        drawing = Drawing(400, 200)
        
        # Create bar chart
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [percentages]
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 20
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = languages
        bc.bars[0].fillColor = COLORS['primary']
        
        drawing.add(bc)
        return drawing

    def _create_intent_recognition_chart(self, data):
        """Create a chart showing intent recognition accuracy.

        Args:
            data: Intent recognition data

        Returns:
            A ReportLab Drawing object containing the chart
        """
        # Count correct recognitions
        correct = sum(1 for item in data if item['actual'] == item['detected'])
        incorrect = len(data) - correct
        
        # Create drawing
        drawing = Drawing(400, 200)
        
        # Create pie chart
        pc = Pie()
        pc.x = 150
        pc.y = 75
        pc.width = 150
        pc.height = 150
        pc.data = [correct, incorrect]
        pc.labels = [f'Correct ({correct})', f'Incorrect ({incorrect})']
        pc.slices.strokeWidth = 0.5
        pc.slices[0].fillColor = COLORS['success']
        pc.slices[1].fillColor = COLORS['danger']
        
        drawing.add(pc)
        return drawing

    def _create_response_quality_chart(self, data):
        """Create a chart showing response quality scores by language.

        Args:
            data: Response quality data

        Returns:
            A ReportLab Drawing object containing the chart
        """
        # Calculate average scores by language
        languages = ['english', 'hindi', 'hinglish']
        scores = {lang: {'total': 0, 'count': 0} for lang in languages}
        
        for item in data:
            lang = item['language']
            score = item['score']
            if lang in scores:
                scores[lang]['total'] += score
                scores[lang]['count'] += 1
        
        # Calculate averages
        averages = []
        for lang in languages:
            if scores[lang]['count'] > 0:
                avg = scores[lang]['total'] / scores[lang]['count']
            else:
                avg = 0
            averages.append(avg)
        
        # Create drawing
        drawing = Drawing(400, 200)
        
        # Create bar chart
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [averages]
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 5
        bc.valueAxis.valueStep = 1
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = languages
        bc.bars[0].fillColor = COLORS['secondary']
        
        drawing.add(bc)
        return drawing

    def _create_command_success_chart(self, data):
        """Create a chart showing command success rates by type.

        Args:
            data: Command success rate data

        Returns:
            A ReportLab Drawing object containing the chart
        """
        # Extract data
        command_types = list(data.keys())
        success_rates = [data[cmd] for cmd in command_types]
        
        # Create drawing
        drawing = Drawing(400, 200)
        
        # Create bar chart
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [success_rates]
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 20
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = command_types
        bc.bars[0].fillColor = COLORS['primary']
        
        drawing.add(bc)
        return drawing

    def _create_test_coverage_chart(self, data):
        """Create a chart showing test coverage by language.

        Args:
            data: Test coverage data

        Returns:
            A ReportLab Drawing object containing the chart
        """
        # Extract data
        languages = list(data.keys())
        counts = [data[lang] for lang in languages]
        
        # Create drawing
        drawing = Drawing(400, 200)
        
        # Create pie chart
        pc = Pie()
        pc.x = 150
        pc.y = 75
        pc.width = 150
        pc.height = 150
        pc.data = counts
        pc.labels = [f'{lang} ({count})' for lang, count in zip(languages, counts)]
        pc.slices.strokeWidth = 0.5
        
        # Set colors for each language
        for i, lang in enumerate(languages):
            if lang in COLORS:
                pc.slices[i].fillColor = COLORS[lang]
        
        drawing.add(pc)
        return drawing

    def _create_issues_table(self, issues):
        """Create a table showing reported issues.

        Args:
            issues: List of issue dictionaries

        Returns:
            A ReportLab Table object
        """
        # Sort issues by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_issues = sorted(issues, key=lambda x: severity_order.get(x['severity'], 4))
        
        # Create table data
        table_data = [
            ['Severity', 'Description', 'Language', 'Command Type']
        ]
        
        for issue in sorted_issues:
            severity = issue['severity'].capitalize()
            description = issue['description']
            language = issue['language'].capitalize()
            command_type = issue['command_type'].capitalize()
            
            table_data.append([severity, description, language, command_type])
        
        # Create table
        table = Table(table_data, colWidths=[1*inch, 3*inch, 1*inch, 1.5*inch])
        
        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['gray']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ])
        
        # Add conditional formatting for severity
        for i, issue in enumerate(sorted_issues, 1):
            severity = issue['severity'].lower()
            if severity == 'critical':
                style.add('BACKGROUND', (0, i), (0, i), COLORS['danger'])
                style.add('TEXTCOLOR', (0, i), (0, i), colors.white)
            elif severity == 'high':
                style.add('BACKGROUND', (0, i), (0, i), COLORS['secondary'])
                style.add('TEXTCOLOR', (0, i), (0, i), colors.white)
            elif severity == 'medium':
                style.add('BACKGROUND', (0, i), (0, i), COLORS['primary'])
                style.add('TEXTCOLOR', (0, i), (0, i), colors.white)
        
        table.setStyle(style)
        return table

    def _create_summary_table(self, data):
        """Create a summary table with key metrics.

        Args:
            data: Test data dictionary

        Returns:
            A ReportLab Table object
        """
        # Calculate metrics
        # Language detection accuracy
        lang_detection = data.get('language_detection', [])
        lang_correct = sum(1 for item in lang_detection if item['actual'] == item['detected'])
        lang_total = len(lang_detection)
        lang_accuracy = (lang_correct / lang_total * 100) if lang_total > 0 else 0
        
        # Intent recognition accuracy
        intent_recognition = data.get('intent_recognition', [])
        intent_correct = sum(1 for item in intent_recognition if item['actual'] == item['detected'])
        intent_total = len(intent_recognition)
        intent_accuracy = (intent_correct / intent_total * 100) if intent_total > 0 else 0
        
        # Response quality average
        response_quality = data.get('response_quality', [])
        response_scores = [item['score'] for item in response_quality]
        response_avg = sum(response_scores) / len(response_scores) if response_scores else 0
        
        # Issues by severity
        issues = data.get('issues', [])
        critical_issues = sum(1 for issue in issues if issue['severity'] == 'critical')
        high_issues = sum(1 for issue in issues if issue['severity'] == 'high')
        medium_issues = sum(1 for issue in issues if issue['severity'] == 'medium')
        low_issues = sum(1 for issue in issues if issue['severity'] == 'low')
        
        # Test coverage
        test_coverage = data.get('test_coverage', {})
        total_tests = sum(test_coverage.values())
        
        # Create table data
        table_data = [
            ['Metric', 'Value'],
            ['Language Detection Accuracy', f'{lang_accuracy:.1f}%'],
            ['Intent Recognition Accuracy', f'{intent_accuracy:.1f}%'],
            ['Average Response Quality', f'{response_avg:.1f}/5.0'],
            ['Total Tests Executed', str(total_tests)],
            ['Critical Issues', str(critical_issues)],
            ['High Priority Issues', str(high_issues)],
            ['Medium Priority Issues', str(medium_issues)],
            ['Low Priority Issues', str(low_issues)],
        ]
        
        # Create table
        table = Table(table_data, colWidths=[3*inch, 1.5*inch])
        
        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['gray']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ])
        
        # Add conditional formatting for metrics
        # Language detection
        if lang_accuracy >= 95:
            style.add('BACKGROUND', (1, 1), (1, 1), COLORS['success'])
            style.add('TEXTCOLOR', (1, 1), (1, 1), colors.white)
        elif lang_accuracy >= 85:
            style.add('BACKGROUND', (1, 1), (1, 1), COLORS['secondary'])
            style.add('TEXTCOLOR', (1, 1), (1, 1), colors.white)
        else:
            style.add('BACKGROUND', (1, 1), (1, 1), COLORS['danger'])
            style.add('TEXTCOLOR', (1, 1), (1, 1), colors.white)
        
        # Intent recognition
        if intent_accuracy >= 90:
            style.add('BACKGROUND', (1, 2), (1, 2), COLORS['success'])
            style.add('TEXTCOLOR', (1, 2), (1, 2), colors.white)
        elif intent_accuracy >= 80:
            style.add('BACKGROUND', (1, 2), (1, 2), COLORS['secondary'])
            style.add('TEXTCOLOR', (1, 2), (1, 2), colors.white)
        else:
            style.add('BACKGROUND', (1, 2), (1, 2), COLORS['danger'])
            style.add('TEXTCOLOR', (1, 2), (1, 2), colors.white)
        
        # Response quality
        if response_avg >= 4.0:
            style.add('BACKGROUND', (1, 3), (1, 3), COLORS['success'])
            style.add('TEXTCOLOR', (1, 3), (1, 3), colors.white)
        elif response_avg >= 3.5:
            style.add('BACKGROUND', (1, 3), (1, 3), COLORS['secondary'])
            style.add('TEXTCOLOR', (1, 3), (1, 3), colors.white)
        else:
            style.add('BACKGROUND', (1, 3), (1, 3), COLORS['danger'])
            style.add('TEXTCOLOR', (1, 3), (1, 3), colors.white)
        
        # Issues
        if critical_issues > 0:
            style.add('BACKGROUND', (1, 5), (1, 5), COLORS['danger'])
            style.add('TEXTCOLOR', (1, 5), (1, 5), colors.white)
        
        if high_issues > 3:
            style.add('BACKGROUND', (1, 6), (1, 6), COLORS['secondary'])
            style.add('TEXTCOLOR', (1, 6), (1, 6), colors.white)
        
        table.setStyle(style)
        return table

    def generate_report(self, date_str, report_type='daily', output_file=None):
        """Generate a PDF test summary report.

        Args:
            date_str: Date string in YYYY-MM-DD format
            report_type: 'daily' or 'weekly'
            output_file: Output file path (optional)

        Returns:
            Path to the generated PDF file
        """
        # Load test data
        data = self._load_test_data(date_str, report_type)
        
        # Determine output file path
        if output_file is None:
            if report_type == 'weekly':
                start_date = data.get('date_range', {}).get('start', date_str)
                end_date = data.get('date_range', {}).get('end', date_str)
                output_file = os.path.join(self.output_dir, f'weekly_test_report_{start_date}_to_{end_date}.pdf')
            else:
                output_file = os.path.join(self.output_dir, f'daily_test_report_{date_str}.pdf')
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_file,
            pagesize=landscape(letter),
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        # Create story (content)
        story = []
        
        # Add title
        if report_type == 'weekly':
            start_date = data.get('date_range', {}).get('start', date_str)
            end_date = data.get('date_range', {}).get('end', date_str)
            title = f"Weekly WhatsApp Chatbot Test Report\n{start_date} to {end_date}"
        else:
            title = f"Daily WhatsApp Chatbot Test Report\n{date_str}"
        
        story.append(Paragraph(title, self.styles['Title']))
        story.append(Spacer(1, 12))
        
        # Add summary section
        story.append(Paragraph("Test Summary", self.styles['SectionHeading']))
        story.append(self._create_summary_table(data))
        story.append(Spacer(1, 24))
        
        # Add language detection section
        story.append(Paragraph("Language Detection Performance", self.styles['SectionHeading']))
        story.append(self._create_language_detection_chart(data.get('language_detection', [])))
        story.append(Spacer(1, 24))
        
        # Add intent recognition section
        story.append(Paragraph("Intent Recognition Performance", self.styles['SectionHeading']))
        story.append(self._create_intent_recognition_chart(data.get('intent_recognition', [])))
        story.append(Spacer(1, 24))
        
        # Add response quality section
        story.append(Paragraph("Response Quality by Language", self.styles['SectionHeading']))
        story.append(self._create_response_quality_chart(data.get('response_quality', [])))
        story.append(Spacer(1, 24))
        
        # Add page break
        story.append(PageBreak())
        
        # Add command success section
        story.append(Paragraph("Command Success Rates", self.styles['SectionHeading']))
        story.append(self._create_command_success_chart(data.get('command_success', {})))
        story.append(Spacer(1, 24))
        
        # Add test coverage section
        story.append(Paragraph("Test Coverage by Language", self.styles['SectionHeading']))
        story.append(self._create_test_coverage_chart(data.get('test_coverage', {})))
        story.append(Spacer(1, 24))
        
        # Add issues section
        story.append(Paragraph("Reported Issues", self.styles['SectionHeading']))
        story.append(self._create_issues_table(data.get('issues', [])))
        
        # Build PDF
        doc.build(story)
        
        print(f"Report generated: {output_file}")
        return output_file


def main():
    """Main function to run the script from command line."""
    parser = argparse.ArgumentParser(description='Generate WhatsApp Chatbot Test Summary PDF Reports')
    parser.add_argument('--type', choices=['daily', 'weekly'], default='daily',
                        help='Report type: daily or weekly')
    parser.add_argument('--date', required=True, help='Date in YYYY-MM-DD format')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--data-dir', help='Directory containing test data files')
    parser.add_argument('--output-dir', help='Directory to save generated PDF reports')
    
    args = parser.parse_args()
    
    # Create generator
    generator = TestSummaryPDFGenerator(
        data_dir=args.data_dir or DEFAULT_DATA_DIR,
        output_dir=args.output_dir or DEFAULT_OUTPUT_DIR
    )
    
    # Generate report
    output_file = generator.generate_report(
        date_str=args.date,
        report_type=args.type,
        output_file=args.output
    )
    
    print(f"Report saved to: {output_file}")


if __name__ == '__main__':
    main()