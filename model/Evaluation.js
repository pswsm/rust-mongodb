const mongoose = require('mongoose')
require('mongoose-type-email')
require('mongoose-type-url')

module.exports = mongoose.model('Evaluation', {
  email: { type: mongoose.SchemaTypes.Email, required: true },
  modelName: { type: String, required: true },
  researchGroup: { type: String, required: true },
  url: { type: mongoose.SchemaTypes.Url, required: false },
  STS_ca: { combined_score: { type: Number, required: true } },
  POS: { F1: { type: Number, required: true } },
  CatalanQA_results: { f1: { type: Number, required: true }, exact: { type: Number, required: true } },
  XQuAD_Ca: { f1: { type: Number, required: true }, exact: { type: Number, required: true } },
  TeCla: { Accuracy: { type: Number, required: true } },
  TECa: { Accuracy: { type: Number, required: true } },
  AnCora_ca: { F1: { type: Number, required: true } },
  sum: { type: Number, required: true }
})
