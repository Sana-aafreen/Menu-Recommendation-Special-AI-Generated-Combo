// routes/feedback.js
router.post('/track', async (req, res) => {
    const { customer_id, item_id, action } = req.body;
    
    let scoreIncrement = 0;
    if (action === 'view') scoreIncrement = 1;
    if (action === 'cart') scoreIncrement = 5;
    // 'ignore' logic: if item was in top 10 but not clicked, we mark it 0 in DB
    
    // Google Sheets Service call to update the 'Interactions' sheet
    await googleSheetsService.updateInteraction(customer_id, item_id, scoreIncrement);
    
    res.json({ success: true, message: `Feedback ${action} recorded` });
});