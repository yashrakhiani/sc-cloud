/**
 * Google Apps Script - Bulk Email Sender
 * Send up to 1,500 emails/day with Google Workspace
 * Deploy via script.google.com
 * 
 * SETUP:
 * 1. Create new Google Sheet with columns: Company, Email, Status, Sent_At
 * 2. Open Tools > Script Editor
 * 3. Paste this code
 * 4. Set up time-driven trigger for daily automation
 * 
 * Author: StructCrew Lead Generation System
 * Updated: Nov 27, 2025
 */


// ========== CONFIGURATION ==========
const CONFIG = {
  // Email settings
  FROM_NAME: 'Your Name',
  SUBJECT_TEMPLATE: 'Architecture Collaboration Opportunity',
  UNSUBSCRIBE_EMAIL: 'your.email@gmail.com',
  
  // Sending limits
  DAILY_LIMIT: 1500,  // Google Workspace limit
  BATCH_SIZE: 100,     // Emails per batch
  DELAY_PER_EMAIL: 2000,  // 2 seconds between emails (milliseconds)
  DELAY_PER_BATCH: 30000, // 30 seconds between batches
  
  // Sheet configuration
  SHEET_NAME: 'Leads',  // Name of your leads sheet
  START_ROW: 2,         // Row to start (skip header)
  
  // Column mapping (1-indexed)
  COL_COMPANY: 1,
  COL_EMAIL: 2,
  COL_STATUS: 3,
  COL_SENT_AT: 4
};


// ========== EMAIL TEMPLATE ==========
function getEmailTemplate(company, email) {
  const html = `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
              color: white; padding: 20px; border-radius: 8px; }
    .content { padding: 20px; background: #f9f9f9; border-radius: 8px; margin: 20px 0; }
    .cta { background: #667eea; color: white; padding: 12px 24px; 
           text-decoration: none; border-radius: 4px; display: inline-block; }
    .footer { font-size: 12px; color: #666; margin-top: 20px; }
    .unsubscribe { color: #999; font-size: 11px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>Hi ${company || 'there'}! 👋</h2>
    </div>
    
    <div class="content">
      <p>I came across your job posting on Instagram (@archijobs), and I'm impressed by the work you're doing!</p>
      
      <p>I'm ${CONFIG.FROM_NAME}, and I specialize in <strong>connecting architecture and design studios with top talent</strong> through StructCrew. We've helped studios like yours:</p>
      
      <ul>
        <li>✅ Find qualified candidates 3x faster</li>
        <li>✅ Reduce recruitment costs by 40%</li>
        <li>✅ Build stronger creative teams</li>
      </ul>
      
      <p>Would you be open to a quick 15-minute chat to explore how we can support your hiring needs?</p>
      
      <p style="text-align: center; margin: 30px 0;">
        <a href="https://calendly.com/your-link" class="cta">Book a Free Consultation</a>
      </p>
      
      <p>Looking forward to connecting!</p>
      
      <p>Best regards,<br>
      <strong>${CONFIG.FROM_NAME}</strong><br>
      Recruitment Specialist | StructCrew<br>
      📧 ${CONFIG.UNSUBSCRIBE_EMAIL}<br>
      🌐 <a href="https://structcrew.com">structcrew.com</a></p>
    </div>
    
    <div class="footer">
      <p class="unsubscribe">
        📌 <strong>Unsubscribe:</strong> Not interested? Simply reply with "UNSUBSCRIBE" and we'll remove you immediately.
        We respect your inbox and comply with CAN-SPAM/GDPR regulations.
      </p>
      <p class="unsubscribe">
        This email was sent to ${email} because you posted a job opening on Instagram. 
        We believe our services could benefit your studio.
      </p>
    </div>
  </div>
</body>
</html>
  `;
  
  return html;
}


// ========== MAIN SENDING FUNCTION ==========
function sendBatchEmails() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  
  if (!sheet) {
    Logger.log(`ERROR: Sheet "${CONFIG.SHEET_NAME}" not found`);
    return;
  }
  
  // Get all data
  const data = sheet.getDataRange().getValues();
  const totalRows = data.length;
  
  // Check quota
  const remainingQuota = MailApp.getRemainingDailyQuota();
  Logger.log(`📊 Remaining quota: ${remainingQuota}`);
  
  if (remainingQuota === 0) {
    Logger.log('⚠️ Daily quota exhausted. Try again tomorrow.');
    return;
  }
  
  let sent = 0;
  let skipped = 0;
  let failed = 0;
  
  // Process rows
  for (let i = CONFIG.START_ROW - 1; i < totalRows && sent < CONFIG.DAILY_LIMIT; i++) {
    const row = data[i];
    const company = row[CONFIG.COL_COMPANY - 1] || 'Team';
    const email = row[CONFIG.COL_EMAIL - 1];
    const status = row[CONFIG.COL_STATUS - 1];
    
    // Skip if no email or already sent
    if (!email || status === 'Sent') {
      skipped++;
      continue;
    }
    
    // Validate email
    if (!isValidEmail(email)) {
      sheet.getRange(i + 1, CONFIG.COL_STATUS).setValue('Invalid Email');
      failed++;
      continue;
    }
    
    // Check quota again
    if (MailApp.getRemainingDailyQuota() <= 0) {
      Logger.log('⚠️ Quota exhausted during send');
      break;
    }
    
    try {
      // Get personalized template
      const htmlBody = getEmailTemplate(company, email);
      const subject = CONFIG.SUBJECT_TEMPLATE.replace('{company}', company);
      
      // Send email
      MailApp.sendEmail({
        to: email,
        subject: subject,
        htmlBody: htmlBody,
        name: CONFIG.FROM_NAME,
        replyTo: CONFIG.UNSUBSCRIBE_EMAIL
      });
      
      // Update sheet
      const timestamp = new Date();
      sheet.getRange(i + 1, CONFIG.COL_STATUS).setValue('Sent');
      sheet.getRange(i + 1, CONFIG.COL_SENT_AT).setValue(timestamp);
      
      sent++;
      Logger.log(`✅ Sent to ${email} (${company})`);
      
      // Delay between emails (anti-spam)
      Utilities.sleep(CONFIG.DELAY_PER_EMAIL);
      
      // Batch delay
      if (sent % CONFIG.BATCH_SIZE === 0) {
        Logger.log(`⏸️ Batch complete. Pausing for ${CONFIG.DELAY_PER_BATCH/1000}s...`);
        Utilities.sleep(CONFIG.DELAY_PER_BATCH);
      }
      
    } catch (error) {
      Logger.log(`❌ Error sending to ${email}: ${error}`);
      sheet.getRange(i + 1, CONFIG.COL_STATUS).setValue('Failed');
      failed++;
    }
  }
  
  // Summary
  const summary = `
  ========================================
  📧 EMAIL CAMPAIGN SUMMARY
  ========================================
  ✅ Sent: ${sent}
  ⏭️ Skipped: ${skipped}
  ❌ Failed: ${failed}
  📊 Remaining Quota: ${MailApp.getRemainingDailyQuota()}
  ========================================
  `;
  
  Logger.log(summary);
  
  // Optional: Send summary email to yourself
  if (sent > 0) {
    MailApp.sendEmail({
      to: CONFIG.UNSUBSCRIBE_EMAIL,
      subject: `✅ Campaign Report: ${sent} emails sent`,
      body: summary
    });
  }
}


// ========== UTILITY FUNCTIONS ==========
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}


function checkQuota() {
  const quota = MailApp.getRemainingDailyQuota();
  Logger.log(`Remaining daily quota: ${quota}`);
  return quota;
}


function resetAllStatuses() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  const lastRow = sheet.getLastRow();
  
  // Clear status and timestamp columns
  sheet.getRange(CONFIG.START_ROW, CONFIG.COL_STATUS, lastRow - 1, 2).clearContent();
  
  Logger.log('✅ All statuses reset');
}


// ========== TIME TRIGGER SETUP ==========
function createDailyTrigger() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));
  
  // Create new daily trigger (runs at 9 AM)
  ScriptApp.newTrigger('sendBatchEmails')
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
  
  Logger.log('✅ Daily trigger created (9 AM)');
}


// ========== TESTING FUNCTIONS ==========
function testSendSingleEmail() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  const testEmail = sheet.getRange(2, CONFIG.COL_EMAIL).getValue();
  const testCompany = sheet.getRange(2, CONFIG.COL_COMPANY).getValue();
  
  Logger.log(`Sending test email to: ${testEmail}`);
  
  try {
    const html = getEmailTemplate(testCompany, testEmail);
    MailApp.sendEmail({
      to: testEmail,
      subject: CONFIG.SUBJECT_TEMPLATE.replace('{company}', testCompany),
      htmlBody: html,
      name: CONFIG.FROM_NAME
    });
    
    Logger.log('✅ Test email sent successfully!');
  } catch (error) {
    Logger.log(`❌ Error: ${error}`);
  }
}


// ========== MENU ==========
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('📧 Email Campaign')
    .addItem('Send Batch Emails', 'sendBatchEmails')
    .addItem('Check Quota', 'checkQuota')
    .addItem('Test Single Email', 'testSendSingleEmail')
    .addSeparator()
    .addItem('Setup Daily Trigger', 'createDailyTrigger')
    .addItem('Reset All Statuses', 'resetAllStatuses')
    .addToUi();
}
