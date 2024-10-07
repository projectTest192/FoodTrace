package main

import (
	"encoding/json"
	"fmt"
	"strconv"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing products
type SmartContract struct {
	contractapi.Contract
}

// Product describes basic details of what makes up a product
type Product struct {
	ID          string `json:"id"`          // 产品ID
	Name        string `json:"name"`        // 产品名称
	Description string `json:"description"` // 产品描述
	Producer    string `json:"producer"`    // 生产商
	ProductDate string `json:"productDate"` // 生产日期
	Status      string `json:"status"`      // 产品状态
	// 出厂记录
	DeviceID    string    `json:"deviceId"`    // 设备ID
	RFIDID      string    `json:"rfidId"`      // RFID标签ID
	Temperature float64   `json:"temperature"` // 出厂温度
	Humidity    float64   `json:"humidity"`    // 出厂湿度
	Latitude    float64   `json:"latitude"`    // 出厂纬度
	Longitude   float64   `json:"longitude"`   // 出厂经度
	WriteTime   time.Time `json:"writeTime"`   // 出厂时间
}

// Init is called during chaincode instantiation to initialize any data
func (s *SmartContract) Init(ctx contractapi.TransactionContextInterface) error {
	fmt.Println("Initializing the chaincode")
	return s.InitLedger(ctx)
}

// InitLedger adds a base set of products to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	// 检查是否已经初始化
	iterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return err
	}
	defer iterator.Close()

	// 如果已经有数据，说明已经初始化过
	if iterator.HasNext() {
		return nil
	}

	// 只有在完全空的账本时才初始化示例数据
	products := []Product{
		{
			ID:          "test001",
			Name:        "test Food",
			Description: "This is a test food product",
			Producer:    "test Producer",
			ProductDate: time.Now().Format("2006-01-02"),
			Status:      "active",
			// 出厂记录
			DeviceID:    "DEV001_test",
			RFIDID:      "RF001_test",
			Temperature: 8.5,
			Humidity:    45.2,
			Latitude:    31.2304,
			Longitude:   121.4737,
			WriteTime:   time.Now(),
		},
	}

	for _, product := range products {
		productJSON, err := json.Marshal(product)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(product.ID, productJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state: %v", err)
		}
	}

	return nil
}

// CreateProduct 创建新产品（包含出厂数据）
func (s *SmartContract) CreateProduct(ctx contractapi.TransactionContextInterface,
	id, name, description, producer, productDate string,
	deviceId, rfidId string,
	temperature, humidity, latitude, longitude string) error {

	exists, err := s.ProductExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("product %s already exists", id)
	}

	product := Product{
		ID:          id,
		Name:        name,
		Description: description,
		Producer:    producer,
		ProductDate: productDate,
		Status:      "active",
		// 出厂数据
		DeviceID:    deviceId,
		RFIDID:      rfidId,
		Temperature: parseFloat64(temperature),
		Humidity:    parseFloat64(humidity),
		Latitude:    parseFloat64(latitude),
		Longitude:   parseFloat64(longitude),
		WriteTime:   time.Now(),
	}

	productJSON, err := json.Marshal(product)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, productJSON)
}

// GetAllProducts returns all products found in world state
func (s *SmartContract) GetAllProducts(ctx contractapi.TransactionContextInterface) ([]*Product, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var products []*Product
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var product Product
		err = json.Unmarshal(queryResponse.Value, &product)
		if err != nil {
			return nil, err
		}
		products = append(products, &product)
	}

	return products, nil
}

// ProductExists returns true when product with given ID exists in world state
func (s *SmartContract) ProductExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	productJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return productJSON != nil, nil
}

// SetProductStatus 设置产品状态
func (s *SmartContract) SetProductStatus(ctx contractapi.TransactionContextInterface, id string, status string) error {
	// 检查产品是否存在
	productJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return fmt.Errorf("failed to read product: %v", err)
	}
	if productJSON == nil {
		return fmt.Errorf("product %s does not exist", id)
	}

	// 解析产品数据
	var product Product
	err = json.Unmarshal(productJSON, &product)
	if err != nil {
		return err
	}

	// 更新状态
	product.Status = status

	// 保存更新后的产品数据
	updatedProductJSON, err := json.Marshal(product)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, updatedProductJSON)
}

// GetActiveProducts 只返回状态为active的产品
func (s *SmartContract) GetActiveProducts(ctx contractapi.TransactionContextInterface) ([]*Product, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var products []*Product
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var product Product
		err = json.Unmarshal(queryResponse.Value, &product)
		if err != nil {
			return nil, err
		}
		if product.Status == "active" {
			products = append(products, &product)
		}
	}

	return products, nil
}

// 辅助函数
func parseInt64(s string) int64 {
	i, _ := strconv.ParseInt(s, 10, 64)
	return i
}

func parseFloat64(s string) float64 {
	f, _ := strconv.ParseFloat(s, 64)
	return f
}

// GetProductHistory 获取产品历史记录
func (s *SmartContract) GetProductHistory(ctx contractapi.TransactionContextInterface, productId string) ([]interface{}, error) {
	// 获取产品历史记录
	historyIterator, err := ctx.GetStub().GetHistoryForKey(productId)
	if err != nil {
		return nil, fmt.Errorf("failed to get history for product %s: %v", productId, err)
	}
	defer historyIterator.Close()

	var records []interface{}
	for historyIterator.HasNext() {
		record, err := historyIterator.Next()
		if err != nil {
			return nil, fmt.Errorf("failed to iterate history: %v", err)
		}

		// 构造历史记录
		var historyRecord struct {
			TxId      string    `json:"txId"`
			Value     Product   `json:"value"`
			Timestamp time.Time `json:"timestamp"`
			IsDelete  bool      `json:"isDelete"`
		}

		historyRecord.TxId = record.TxId
		historyRecord.Timestamp = time.Unix(record.Timestamp.Seconds, int64(record.Timestamp.Nanos))
		historyRecord.IsDelete = record.IsDelete

		if record.Value != nil {
			var product Product
			if err := json.Unmarshal(record.Value, &product); err != nil {
				return nil, fmt.Errorf("failed to unmarshal product: %v", err)
			}
			historyRecord.Value = product
		}

		records = append(records, historyRecord)
	}

	return records, nil
}

// 按状态查询产品
func (s *SmartContract) GetProductsByStatus(ctx contractapi.TransactionContextInterface, status string) ([]*Product, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var products []*Product
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var product Product
		err = json.Unmarshal(queryResponse.Value, &product)
		if err != nil {
			return nil, err
		}
		if product.Status == status {
			products = append(products, &product)
		}
	}

	return products, nil
}

// 按生产商查询产品
func (s *SmartContract) GetProductsByProducer(ctx contractapi.TransactionContextInterface, producer string) ([]*Product, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var products []*Product
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var product Product
		err = json.Unmarshal(queryResponse.Value, &product)
		if err != nil {
			return nil, err
		}
		if product.Producer == producer {
			products = append(products, &product)
		}
	}

	return products, nil
}

// 按时间范围查询产品
func (s *SmartContract) GetProductsByDateRange(ctx contractapi.TransactionContextInterface, startDate string, endDate string) ([]*Product, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var products []*Product
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var product Product
		err = json.Unmarshal(queryResponse.Value, &product)
		if err != nil {
			return nil, err
		}

		// 检查日期范围
		if product.ProductDate >= startDate && product.ProductDate <= endDate {
			products = append(products, &product)
		}
	}

	return products, nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(new(SmartContract))
	if err != nil {
		fmt.Printf("Error creating chaincode: %v\n", err)
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting chaincode: %v\n", err)
	}
}
