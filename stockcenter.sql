-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 27/02/2025 às 01:04
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `stockcenter`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `itens`
--

CREATE TABLE `itens` (
  `id_item` int(11) NOT NULL,
  `codigo_barras` varchar(50) NOT NULL,
  `nome_item` varchar(100) NOT NULL,
  `descricao` text DEFAULT NULL,
  `quantidade` int(11) NOT NULL DEFAULT 0,
  `id_local` int(11) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `itens`
--

INSERT INTO `itens` (`id_item`, `codigo_barras`, `nome_item`, `descricao`, `quantidade`, `id_local`, `id_user`) VALUES
(13, '87612312', 'teste', 'teste', 1, 5, NULL);

--
-- Acionadores `itens`
--
DELIMITER $$
CREATE TRIGGER `trg_itens_auditoria_delete` AFTER DELETE ON `itens` FOR EACH ROW BEGIN
    INSERT INTO Logs_Auditoria (id_user, acao, detalhes)
    VALUES (OLD.id_user, 'DELETE', CONCAT('Item removido: ID ', OLD.id_item));
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_itens_auditoria_insert` AFTER INSERT ON `itens` FOR EACH ROW BEGIN
    INSERT INTO Logs_Auditoria (id_user, acao, detalhes)
    VALUES (NEW.id_user, 'INSERT', CONCAT('Item inserido: ID ', NEW.id_item));
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_registrar_movimentacao` AFTER UPDATE ON `itens` FOR EACH ROW BEGIN
    -- Verifica se o local do item foi alterado
    IF OLD.id_local <> NEW.id_local THEN
        INSERT INTO Movimentacoes (id_item, id_local_origem, id_local_destino, quantidade, id_user)
        VALUES (
            NEW.id_item, 
            OLD.id_local, 
            NEW.id_local, 
            1,  -- Ajuste se houver uma quantidade associada à movimentação
            NEW.id_user  -- Ajuste conforme a estrutura da tabela Itens
        );
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `locais`
--

CREATE TABLE `locais` (
  `id_local` int(11) NOT NULL,
  `nome_local` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `locais`
--

INSERT INTO `locais` (`id_local`, `nome_local`) VALUES
(5, 'galpao5'),
(6, 'galpao1');

-- --------------------------------------------------------

--
-- Estrutura para tabela `logs_auditoria`
--

CREATE TABLE `logs_auditoria` (
  `id_log` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `data_hora` datetime DEFAULT current_timestamp(),
  `acao` varchar(50) NOT NULL,
  `detalhes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `logs_auditoria`
--

INSERT INTO `logs_auditoria` (`id_log`, `id_user`, `data_hora`, `acao`, `detalhes`) VALUES
(23, NULL, '2025-02-26 21:01:13', 'INSERT', 'Item inserido: ID 13'),
(24, NULL, '2025-02-26 21:03:32', 'INSERT', 'Item inserido: ID 14'),
(25, NULL, '2025-02-26 21:03:48', 'DELETE', 'Item removido: ID 14');

-- --------------------------------------------------------

--
-- Estrutura para tabela `movimentacoes`
--

CREATE TABLE `movimentacoes` (
  `id_mov` int(11) NOT NULL,
  `id_item` int(11) DEFAULT NULL,
  `id_local_origem` int(11) DEFAULT NULL,
  `id_local_destino` int(11) DEFAULT NULL,
  `quantidade` int(11) NOT NULL,
  `data_hora` datetime DEFAULT current_timestamp(),
  `id_user` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `movimentacoes`
--

INSERT INTO `movimentacoes` (`id_mov`, `id_item`, `id_local_origem`, `id_local_destino`, `quantidade`, `data_hora`, `id_user`) VALUES
(8, 13, 6, 5, 1, '2025-02-26 21:01:51', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id_user` int(11) NOT NULL,
  `nome_user` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `perfil` enum('Administrador','Gerente','Operador') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuarios`
--

INSERT INTO `usuarios` (`id_user`, `nome_user`, `senha`, `perfil`) VALUES
(1, 'admin', '1234', 'Administrador'),
(5, 'gerente', '1234', 'Gerente'),
(6, 'operador', '1234', 'Operador');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `itens`
--
ALTER TABLE `itens`
  ADD PRIMARY KEY (`id_item`),
  ADD UNIQUE KEY `codigo_barras` (`codigo_barras`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_local` (`id_local`);

--
-- Índices de tabela `locais`
--
ALTER TABLE `locais`
  ADD PRIMARY KEY (`id_local`);

--
-- Índices de tabela `logs_auditoria`
--
ALTER TABLE `logs_auditoria`
  ADD PRIMARY KEY (`id_log`),
  ADD KEY `id_user` (`id_user`);

--
-- Índices de tabela `movimentacoes`
--
ALTER TABLE `movimentacoes`
  ADD PRIMARY KEY (`id_mov`),
  ADD KEY `id_item` (`id_item`),
  ADD KEY `id_local_origem` (`id_local_origem`),
  ADD KEY `id_local_destino` (`id_local_destino`),
  ADD KEY `id_user` (`id_user`);

--
-- Índices de tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `itens`
--
ALTER TABLE `itens`
  MODIFY `id_item` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de tabela `locais`
--
ALTER TABLE `locais`
  MODIFY `id_local` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `logs_auditoria`
--
ALTER TABLE `logs_auditoria`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de tabela `movimentacoes`
--
ALTER TABLE `movimentacoes`
  MODIFY `id_mov` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `itens`
--
ALTER TABLE `itens`
  ADD CONSTRAINT `itens_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `usuarios` (`id_user`),
  ADD CONSTRAINT `itens_ibfk_2` FOREIGN KEY (`id_local`) REFERENCES `locais` (`id_local`);

--
-- Restrições para tabelas `logs_auditoria`
--
ALTER TABLE `logs_auditoria`
  ADD CONSTRAINT `logs_auditoria_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `usuarios` (`id_user`);

--
-- Restrições para tabelas `movimentacoes`
--
ALTER TABLE `movimentacoes`
  ADD CONSTRAINT `movimentacoes_ibfk_1` FOREIGN KEY (`id_item`) REFERENCES `itens` (`id_item`),
  ADD CONSTRAINT `movimentacoes_ibfk_2` FOREIGN KEY (`id_local_origem`) REFERENCES `locais` (`id_local`),
  ADD CONSTRAINT `movimentacoes_ibfk_3` FOREIGN KEY (`id_local_destino`) REFERENCES `locais` (`id_local`),
  ADD CONSTRAINT `movimentacoes_ibfk_4` FOREIGN KEY (`id_user`) REFERENCES `usuarios` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
